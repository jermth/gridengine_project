#
# Cookbook Name:: csge
# Recipe:: sgemaster
#
# The SGE Master is a Q-Master and a Submitter 
#

Chef::Log.warn("This recipe has been decprecated. Please use csge::master instead")
include_recipe "csge::master"

