#!/usr/bin/env python
#
# This script creates Ephemeral sequenved zodes
#


import commands
import json
import logging
import os
import random
import signal
import sys
import time


import core


#
# Return the current IP address
#
def getIP():
	retval = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
	return(retval)


zk = core.connect()
data = {}
data["ip"] = getIP()
data["pid"] = os.getpid()


key = zk.create(core.key + "/testseq-", json.dumps(data), ephemeral=True, sequence=True)
logging.info("Inserted IP and PID into key '%s'" % key)

#
# Sleep for a random number of seconds
#
num_secs = random.randint(5, 60)

logging.info("Sleeping for %d seconds..." % num_secs)
time.sleep(num_secs)

logging.info("Woke up! Deleting our key and disconnecting.")
zk.delete(key)


