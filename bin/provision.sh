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

FILE="/var/apt-get-update"
if test -f ${FILE}
then

	FOUND=`find ${FILE} -mmin +${MINUTES}`
	if test "$FOUND"
	then
		echo "# "
		echo "# apt-get update hasn't been run in ${MINUTES} minutes. Running."
		echo "# "
		apt-get update
		touch ${FILE}

	fi

fi


apt-get install -y python-setuptools zookeeper zookeeperd
easy_install pip
pip install -r /vagrant/requirements.txt

PROCESSES=$(pgrep -f zookeeper || true)
if test ! "$PROCESSES"
then
	echo "# "
	echo "# Zookeeper doesn't seem to be running."
	echo "# Starting Zookeeper..."
	echo "# "
	service zookeeper start
fi

