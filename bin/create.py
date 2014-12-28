#!/usr/bin/env python
#
# This script creates Ephemeral sequenced zodes
#
"""
Usage: create.py [SECONDS]

	-h, --help		Show this help section
	SECONDS			How many seconds to stay running for?
					If this is not specified, a random value is used


"""


import commands
import json
import logging
import os
import random
import signal
import sys
import time

from docopt import docopt

import core


#
# Return the current IP address
#
def getIP():
	retval = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
	return(retval)

params = docopt(__doc__, version='0.1.0 alpha')


zk = core.connect()
data = {}
data["ip"] = getIP()
data["pid"] = os.getpid()


key = zk.create(core.key + "/testseq-", json.dumps(data), ephemeral=True, sequence=True)
logging.info("Inserted IP and PID into key '%s'" % key)

num_secs = int(params["SECONDS"])
if (not num_secs):
	num_secs = random.randint(5, 60)

logging.info("Sleeping for %d seconds..." % num_secs)
time.sleep(num_secs)

logging.info("Woke up! Deleting our key and disconnecting.")
zk.delete(key)


