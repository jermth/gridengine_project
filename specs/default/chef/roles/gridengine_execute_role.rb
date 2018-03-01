name "gridengine_execute_role"
description "GridEngine Client Role"
run_list("recipe[cshared::client]",
  "recipe[cuser]",
  "recipe[csge::execute]",
  "recipe[cycle_server::submit_once_workers]")

default_attributes(
  "gridengine" => { "make" => "ge", "version" => "8.5.0", "root" => "/sched/ge/ge-8.5.0" }
)
