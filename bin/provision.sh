#!/bin/bash
#
# Provision our Vagrant instance
#


#
# Errors are fatal
#
set -e


MINUTES=1440
#MINUTES=10 # Debugging
#MINUTES=1 # Debugging
FOUND=`find /var/apt-get-update -mmin +${MINUTES}`
if test "$FOUND"
then
	echo "# "
	echo "# apt-get update hasn't been run in ${MINUTES} minutes. Running."
	echo "# "
	apt-get update
	touch /var/apt-get-update
fi


apt-get install -y python-setuptools zookeeper
easy_install pip
pip install -r /vagrant/requirements.txt

/usr/share/zookeeper/bin/zkServer.sh start

