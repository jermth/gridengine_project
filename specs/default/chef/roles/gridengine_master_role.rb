name "gridengine_master_role"
description "GridEngine Master Role"
run_list("role[scheduler]",
  "recipe[cshared::directories]",
  "recipe[cuser]",
  "recipe[cshared::server]",
  "recipe[csge::master]")

default_attributes(
  "cyclecloud" => { "discoverable" => true },
  "gridengine" => { "make" => "ge", "version" => "8.5.0", "root" => "/sched/ge/ge-8.5.0" }
)
