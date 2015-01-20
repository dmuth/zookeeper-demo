#!/bin/bash
#
# Provision a Vagrant instance to run multiple instances of Zookeeper for testing purposes
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

echo "# "
echo "# Creating and enabling our swapfile"
echo "# "
SWAPFILE="/swapfile"
if test ! -f ${SWAPFILE}
then
	fallocate -l 1G ${SWAPFILE}
fi

chmod 600 ${SWAPFILE}
mkswap ${SWAPFILE}
swapon ${SWAPFILE} || true

echo "# "
echo "# Note that the swap won't survive a reboot. "
echo "# You'll need to rerun this provision script at reboot."
echo "# "



echo "# " 
echo "# Installing Zookeeper and our necesary Python modules" 
echo "# " 
apt-get install -y python-setuptools zookeeper
easy_install pip
pip install -r /vagrant/requirements.txt

echo "# " 
echo "# Installing Zookeeper config" 
echo "# " 

cp -r /vagrant/conf/multi /etc/zookeeper/conf

mkdir -p /var/lib/zookeeper/data0
mkdir -p /var/lib/zookeeper/data1
mkdir -p /var/lib/zookeeper/data2

echo 0 > /var/lib/zookeeper/data0/myid
echo 1 > /var/lib/zookeeper/data1/myid
echo 2 > /var/lib/zookeeper/data2/myid

echo "# "
echo "# Starting Zookeeper processes"
echo "# "
/usr/share/zookeeper/bin/zkServer.sh restart /etc/zookeeper/conf/multi/0.conf
/usr/share/zookeeper/bin/zkServer.sh restart /etc/zookeeper/conf/multi/1.conf
/usr/share/zookeeper/bin/zkServer.sh restart /etc/zookeeper/conf/multi/2.conf


