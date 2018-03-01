#!/usr/bin/env python
from sge import get_sge_job_details, get_host_complexes
import subprocess
import sys
import os
import datetime
import jetpack.config

jobs_by_affinity_group = {}

# Check to see if modify_jobs.py is already running. If it is then exit, otherwise remove the old pidfile (if it exists) and
# create a new one.
def makePidfile(pidfile):
    pid = str(os.getpid())
    if os.path.isfile(pidfile):
        oldpid = int(open(pidfile).readline())
        try:
            os.kill(oldpid,0)
            print "Already running, exiting."
            sys.exit()
        except OSError:
            print "Found stale pidfile, continuing anyway."
            os.unlink(pidfile)
    file(pidfile, 'w').write(pid)

# Load up a user-defined function to parse JobDetail dictionaries and pass back attributes to update a job already in the queue
# specifically the slot_type if it isn't defined, but other attributes can be passed back as well. If the user-defined function
# doesn't exist, use our own which always returns the input and a slot_type of 'execute'
def sge_job_handler(job_details):
    """ Takes in a 'job_details' and returns a potentially updated job details object...

    TODO: What are they really allowed to update? Just hard resources "-l <foo>=<bar>"???
    """
    def _get(name):
        """ Does the name exist in hard or soft resources """
        if 'hard_resources' in job_details and name in job_details['hard_resources']:
            return job_details['hard_resources'][name]
        elif 'soft_resources' in job_details and name in job_details['soft_resources']:
            return job_details['soft_resources'][name]
        else:
            return None

    details = {}

    # Set the slot type if it isn't already set
    slot_type = _get('slot_type')
    if slot_type is None:
        slot_type = 'execute'
        details['slot_type'] = slot_type

    # Set the affinity group if grouping is enabled, it isn't already set
    # and it's a MPI job
    groups_enabled = jetpack.config.get('cyclecloud.cluster.autoscale.use_node_groups')
    affinity_group = _get('affinity_group')
    if groups_enabled and affinity_group is None and 'pe_range' in job_details and 'min' in job_details['pe_range']:
        # Find an affinity_group for the node
        job_size = job_details['pe_range']['min']
        if len(jobs_by_affinity_group) == 0:
            for job_id, job in get_sge_job_details().iteritems():
                st = None
                ag = None
                if 'hard_resources' in job and 'slot_type' in job['hard_resources']:
                    st = job['hard_resources']['slot_type']
                elif 'soft_resources' in job and 'slot_type' in job['soft_resources']:
                    st = job['soft_resources']['slot_type']
                
                if 'hard_resources' in job and 'affinity_group' in job['hard_resources']:
                    ag = job['hard_resources']['affinity_group']
                elif 'soft_resources' in job and 'affinity_group' in job['soft_resources']:
                    ag = job['soft_resources']['affinity_group']
                
                if st and ag:
                    jobs_by_affinity_group[(st, ag)] = job_id

        
        host_complexes = get_host_complexes(['slot_type', 'affinity_group', 'affinity_group_cores'])
        affinity_groups = [hc['affinity_group'] for hc in host_complexes.itervalues() if hc['slot_type'] == slot_type and hc['affinity_group'] not in [None, 'default'] and int(float(hc['affinity_group_cores'] or 0)) == int(job_size)]
        for g in affinity_groups:
            if (slot_type, g) in jobs_by_affinity_group:
                continue
            else:
                jobs_by_affinity_group[(slot_type, g)] = job_details['job_number']
                details['affinity_group'] = g
                break
    else:
        # We just use 'default' for the affinity group
        details['affinity_group'] = affinity_group or 'default'

    return details

try:
    sys.path.append("/opt/cycle/jetpack/config")
    from autoscale import sge_job_handler  # This should always fail - "blah" should be a module name that we define for all autoscaling stuff
except ImportError:
    pass  # The default function above will be used instead

if __name__ == "__main__":

    print "%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pidfile = "/var/run/modify_jobs.pid"
    makePidfile(pidfile)


    job_details = get_sge_job_details()
    # Check for updates to the job

    resources = {}
    for job_detail in job_details.itervalues():
        updates = sge_job_handler(job_detail)
        updates_to_apply = {}
        # Check the updates that were sent back to make sure they aren't already set, no need to reset them
        for k, v in updates.iteritems():
            if k in job_detail['hard_resources'] and job_detail['hard_resources'][k] == v:
                pass
            else:
                updates_to_apply[k] = v

        if updates_to_apply:

            # Update the job details
            job_detail['hard_resources'].update(updates_to_apply)

            # Build up the command line and use that as a key to group up jobs with the same command
            command = ""
            for k, v in job_detail['hard_resources'].iteritems():
                command += "%s=%s," % (k, v)

            if command not in resources:
                resources[command] = []
            resources[command].append(job_detail['job_number'])

    # For each group of updates, apply them to all jobs in bulk for speed
    for command, jobs in resources.iteritems():
        command = ". /etc/cluster-setup.sh && qalter %s -l %s" % (",".join([str(j) for j in jobs]), command)
        subprocess.check_call(command, shell=True)

    # Clean up our pidfile so another instance can start
    os.unlink(pidfile)
