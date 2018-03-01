name             "csge"
maintainer       "Cycle Computing"
maintainer_email "cyclecloud-support@cyclecomputing.com"
license          "Apache 2.0"
description      "Installs/Configures csge"
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          "0.1"

%w{ cuser cganglia cycle_server cshared cyclecloud-base }.each {|c| depends c }
