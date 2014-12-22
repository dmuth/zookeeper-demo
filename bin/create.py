#!/usr/bin/env python
#
# This script creates Ephemeral sequenved zodes
#


import commands
import json
import logging
import os
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

#
# Bails out when we get a signal
#
def signal_handler(signal, frame):
	logging.info("Ctrl-C received. Deleting key")
	zk.delete(key)
	sys.exit(0)


zk = core.connect()
data = {}
data["ip"] = getIP()
data["pid"] = os.getpid()


key = zk.create(core.key + "/testseq-", json.dumps(data), ephemeral=True, sequence=True)
logging.info("Inserted IP and PID into key '%s'" % key)

logging.info("Just hanging out because these are emphemeral keys. Press ^C to exit...")

#
# Wait for the user to press ctrl-C
#
signal.signal(signal.SIGINT, signal_handler)
signal.pause()



