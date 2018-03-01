#!/usr/bin/env python

from sge import get_sge_jobs, get_sge_job_details
import jetpack.config

def _get_jobs():
    job_details = get_sge_job_details()
    jobs = get_sge_jobs()

    # Process all the jobs
    autoscale_jobs = []
    for job in jobs:

        # Ignore jobs in "held" or "error" states
        if "h" in job["job_state"] or "e" in job["job_state"]:
            continue

        detail = job_details[job["job_number"]]

        slot_type = None
        if 'hard_resources' in detail:
            slot_type = detail["hard_resources"].get("slot_type", None)

        slots_per_job = 1
        if 'pe_range' in detail and 'min' in detail['pe_range']:
            slots_per_job = int(detail['pe_range']['min'])

        average_runtime = None
        if 'context' in detail and 'average_runtime' in detail['context']:
            average_runtime = int(detail['context']['average_runtime'])
        
        job = {
            'name': job['job_number'],
            'nodearray': slot_type,
            'request_cpus': slots_per_job,
            'average_runtime': average_runtime
        }

        # If it's an MPI job and grouping is enabled
        # we want to use a grouped request to get tightly coupled nodes
        if slots_per_job > 1 and jetpack.config.get('cyclecloud.cluster.autoscale.use_node_groups') is True:
            job['grouped'] = True

        autoscale_jobs.append(job)

    return autoscale_jobs

if __name__ == "__main__":
    import jetpack.autoscale
    jetpack.autoscale.scale_by_jobs(_get_jobs())
