default[:gridengine][:make] = "sge"
default[:gridengine][:version] = "2011.11"
default[:gridengine][:root] = "/sched/sge/sge-2011.11"
default[:gridengine][:package_extension] = "tar.gz"

default[:gridengine][:shared][:bin] = true
default[:gridengine][:shared][:spool] = true

default[:gridengine][:slots] = nil
default[:gridengine][:slot_type] = nil

default[:gridengine][:ignore_fqdn] = true

# Grid engine user settings
default[:gridengine][:group][:name] = "sgeadmin"
default[:gridengine][:group][:gid] = 536

default[:gridengine][:user][:name] = "sgeadmin"
default[:gridengine][:user][:description] = "SGE admin user"
default[:gridengine][:user][:home] = "/shared/home/sgeadmin"
default[:gridengine][:user][:shell] = "/bin/bash"
default[:gridengine][:user][:uid] = 536
default[:gridengine][:user][:gid] = node[:gridengine][:group][:gid]

# List of installed applications for use in SubmitOnce routing
default[:submitonce][:applications] = nil
