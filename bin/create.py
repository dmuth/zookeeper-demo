#!/usr/bin/env python
#
# This script creates Ephemeral sequenved zodes
#


import commands
import json
import logging
import os
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

logging.info("Just hanging out because these are emphemeral keys. Press ^C to exit...")

#
# Just hang out, since the key is ephemeral
#
while 1:
	time.sleep(3600)


