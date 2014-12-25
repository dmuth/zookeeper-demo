# -*- mode: ruby -*-
# vi: set ft=ruby :

#
# Sample command line for bringing up an instance and configuring it:
#

Vagrant.configure("2") do |config|

	#
	# Cache anything we download with apt-get
	#
	if Vagrant.has_plugin?("vagrant-cachier")
		config.cache.scope = :box
	end



	config.vm.define :zoo1 do |host|

		host.vm.box = "trusty64"
		host.vm.box_url = "https://oss-binaries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-amd64-vbox.box"
		host.vm.hostname = "zoo1"
		host.vm.network "private_network", ip: "10.0.10.101"

		#
		# Set the amount of RAM and CPU cores
		#
		host.vm.provider "virtualbox" do |v|
			v.memory = 256
			v.cpus = 2
		end

		#
		# No good can come from updating plugins.
		# Plus, this makes creating Vagrant instances MUCH faster
		#
		if Vagrant.has_plugin?("vagrant-vbguest")
			config.vbguest.auto_update = false
		end

		#
		# Provision this instance
		#
		host.vm.provision "shell", path: "./bin/provision.sh"

	end


	config.vm.define :zoo2 do |host|

		host.vm.box = "trusty64"
		host.vm.box_url = "https://oss-binaries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-amd64-vbox.box"
		host.vm.hostname = "zoo2"
		host.vm.network "private_network", ip: "10.0.10.102"

		#
		# Set the amount of RAM and CPU cores
		#
		host.vm.provider "virtualbox" do |v|
			v.memory = 256
			v.cpus = 2
		end

		#
		# Updating the plugins at start time never ends well.
		#
		if Vagrant.has_plugin?("vagrant-vbguest")
			config.vbguest.auto_update = false
		end

		#
		# Provision this instance
		#
		host.vm.provision "shell", path: "./bin/provision.sh"

	end

	config.vm.define :zoo3 do |host|

		host.vm.box = "trusty64"
		host.vm.box_url = "https://oss-binaries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-amd64-vbox.box"
		host.vm.hostname = "zoo3"
		host.vm.network "private_network", ip: "10.0.10.103"

		#
		# Set the amount of RAM and CPU cores
		#
		host.vm.provider "virtualbox" do |v|
			v.memory = 256
			v.cpus = 2
		end

		#
		# Updating the plugins at start time never ends well.
		#
		if Vagrant.has_plugin?("vagrant-vbguest")
			config.vbguest.auto_update = false
		end

		#
		# Provision this instance
		#
		host.vm.provision "shell", path: "./bin/provision.sh"

	end


end


