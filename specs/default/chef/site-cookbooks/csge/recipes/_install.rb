#
# Cookbook Name:: csge
# Recipe:: _install
#
# For installing SGE on master and compute nodes.
#


sgemake = node[:gridengine][:make]     # ge, sge
sgever = node[:gridengine][:version]   # 8.2.0-demo (ge), 8.2.1 (ge), 6_2u6 (sge), 2011.11 (sge, 8.1.8 (sge)
sgeroot = node[:gridengine][:root] 


sgebins = { 'sge' => %w[64 common] }
sgebins.default = %w[bin-lx-amd64 common]

sgeext = node[:gridengine][:package_extension]

if node[:gridengine][:make] == "sge"
  sgeext = "tgz"
  sgebins[sgemake].each do |arch|
    jetpack_download "#{sgemake}-#{sgever}-#{arch}.#{sgeext}" do
      project "gridengine"
      thunderball_url "cycle/#{sgemake}-#{sgever}-#{arch}.#{sgeext}"
    end
  end
else
  sgebins[sgemake].each do |arch|
    jetpack_download "#{sgemake}-#{sgever}-#{arch}.#{sgeext}" do
      project "gridengine"
    end
  end
end

execute "untarcommon" do
  command "tar -xf #{node[:jetpack][:downloads]}/#{sgemake}-#{sgever}-common.#{sgeext} -C #{sgeroot}"
  creates "#{sgeroot}/inst_sge"
  action :run
end

sgebins[sgemake][0..-2].each do |myarch|

  execute "untar #{sgemake}-#{sgever}-#{myarch}.#{sgeext}" do
    command "tar -xf #{node[:jetpack][:downloads]}/#{sgemake}-#{sgever}-#{myarch}.#{sgeext} -C #{sgeroot}"
    case sgemake
    when "ge"
      strip_bin = myarch.slice!(4..-1)
      creates "#{sgeroot}/bin/#{strip_bin}"
    when "sge"
      strip_bin = myarch.slice!(-3..-1)
      case strip_bin
      when "64"
        creates "#{sgeroot}/bin/linux-x64"
      when "32"
        creates "#{sgeroot}/bin/linux-x86"
      end
    end
    action :run
  end

end
