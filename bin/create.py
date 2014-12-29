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


#
# Return the current IP address
#
def getIP():
	retval = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
	return(retval)


params = docopt(__doc__)
num_secs = 0
if (params["SECONDS"]):
	num_secs = int(params["SECONDS"])


#
# Connect to Zookeeper and create our node
#
zk = core.connect()
data = {}
data["ip"] = getIP()
data["pid"] = os.getpid()

key = zk.create(core.key + "/testseq-", json.dumps(data), ephemeral=True, sequence=True)
key_parts = key.split("/")
our_key = key_parts[len(key_parts) - 1]
logging.info("Inserted IP and PID into key '%s' (our_key=%s)" % (key, our_key) )


#
# This function sets up a watch on a Node.
# Because a watcher function is called when it is assigned and an 
# unlimited number of times when a node changes (or is deleted), 
# we need to have a little wrapper which ensures that a specific 
# node can only be watched ONCE.
#
@core.static_var("watched", {})
def watchNode(our_key, node_to_watch):

	if node_to_watch in watchNode.watched:
		return False
	
	watchNode.watched = node_to_watch
	logging.info("Watching key: %s" % node_to_watch)

	@zk.DataWatch(node_to_watch)
	def watch_node(data, stat):
		#print("watch_node(): data", data, stat)
		logging.info("Change detected in node '%s'" % node_to_watch)
		isMasterNode(our_key)


#
# Get our children and determine if we are the master (first) node.
# If not, watch the node immediately before this one.
#
def isMasterNode(our_key):

	children = zk.get_children(core.key)
	children = sorted(children)

	if (children[0] == our_key):
		logging.info("We're the master node!")

	else:
		last_node = ""
		for child in children:
			if (child == our_key):
				node_to_watch = core.key + "/" + last_node
				logging.info("Found our key, watching the previous key (%s)" % node_to_watch)
				watchNode(our_key, node_to_watch)
				break

			last_node = child

isMasterNode(our_key)



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


