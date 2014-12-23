#!/bin/bash
#
# This script will spawn server create.py processes in an infinite loop
#

if test ! "$1"
then
	echo "Syntax: $0 (num processes to run)"
	exit 1
fi

NUM=$1

#
# Change into where this script lives
#
pushd `dirname $0`

echo "$0: Starting ${NUM} processes (run create-stop.sh to kill them...)"

for I in `seq ${NUM}`
do
	while true; do ./create.py; sleep 1; done &
done



