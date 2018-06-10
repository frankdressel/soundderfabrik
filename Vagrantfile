# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<-SCRIPT
apt-get update
apt-get install -y alsa-oss alsa-utils
apt-get install -y ansible
apt-get install -y git
apt-get install -y xserver-xorg xserver-xorg-core xfonts-base xinit --no-install-recommends
apt-get install -y mate-desktop-environment-core
apt-get install -y lightdm
SCRIPT
  
# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  config.vm.box = "debian/stretch64"
  
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"

  config.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
	  vb.gui=true
  end
  
  config.vm.provision "shell", inline: $script
  
end
