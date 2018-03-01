name "gridengine_master_nofiler_role"
description "GridEngine Master, but not the NFS server"
run_list("role[scheduler]",
  "recipe[cshared::client]",
  "recipe[cuser]",
  "recipe[csge::master]")

default_attributes(
  "cyclecloud" => { "discoverable" => true },
  "gridengine" => { "make" => "ge", "version" => "8.5.0", "root" => "/sched/ge/ge-8.5.0" }
)

