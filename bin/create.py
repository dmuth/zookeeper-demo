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
# Bails out when we get a signal
#
def signal_handler(signal, frame):
	logging.info("Ctrl-C received. Deleting key")
	zk.delete(key)
	sys.exit(0)


params = docopt(__doc__)
num_secs = 0
if (params["SECONDS"]):
	num_secs = int(params["SECONDS"])


#
# Connect to Zookeeper and create our node
#
zk = core.connect()
data = {}
data["ip"] = core.getIP()
data["pid"] = os.getpid()

key = zk.create(core.key + "/testseq-", json.dumps(data), ephemeral=True, sequence=True)
key_parts = key.split("/")
our_key = key_parts[len(key_parts) - 1]
logging.info("Inserted IP and PID into key '%s' (our_key=%s)" % (key, our_key) )


#
# Our worker function to be run when a node is changed
#
def watch_node_worker(data, stat, node_to_watch):
	#print("watch_node(): data", data)
	logging.info("Change detected in node '%s'" % node_to_watch)
	core.isMasterNode(zk, our_key, watch_node_worker)

#
# First check to see if we're the master or not
#
core.isMasterNode(zk, our_key, watch_node_worker)


#
# Sleep for a specific number of seconds
#
if (not num_secs):
	num_secs = random.randint(5, 60)

logging.info("Sleeping for %d seconds..." % num_secs)
signal.signal(signal.SIGINT, signal_handler)
time.sleep(num_secs)


logging.info("Woke up! Deleting our key and disconnecting.")
zk.delete(key)


