#!/usr/bin/env python
#
# This script creates Ephemeral sequenced zodes
#
"""
Usage: create.py [SECONDS] [--host=<hostname>]

	-h, --help		Show this help section
	SECONDS			How many seconds to stay running for?
				If this is not specified, a random value is used
	--host=<hostname>	The hostname and port to connect to [default: 127.0.0.1:2181]


"""


import commands
import logging
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
	zk.delete(key_full)
	sys.exit(0)


params = docopt(__doc__)
num_secs = 0
if (params["SECONDS"]):
	num_secs = int(params["SECONDS"])
if not params["--host"]:
	params["--host"] = "127.0.0.1:2181"


#
# Connect to Zookeeper and create our node
#
zk = core.connect(params["--host"])

(key_full, key_local) = core.createKey(zk)

#
# Our worker function to be run when a node is changed
#
def watch_node_worker(data, stat, node_to_watch):
	#print("watch_node(): data", data)
	logging.info("Change detected in node '%s'" % node_to_watch)
	core.is_master_node(zk, key_local, watch_node_worker)


#
# First check to see if we're the master or not
#
core.is_master_node(zk, key_local, watch_node_worker)


#
# Sleep for a specific number of seconds
#
if (not num_secs):
	num_secs = random.randint(5, 60)

logging.info("Sleeping for %d seconds..." % num_secs)
signal.signal(signal.SIGINT, signal_handler)
time.sleep(num_secs)


logging.info("Woke up! Deleting our key and disconnecting.")
zk.delete(key_full)


