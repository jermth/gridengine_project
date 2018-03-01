#
# Cookbook Name:: csge
# Recipe:: sgeexec
#

Chef::Log.warn("This recipe has been decprecated. Please use csge::execute instead")
include_recipe "csge::execute"
