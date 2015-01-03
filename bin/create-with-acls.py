#!/usr/bin/env python
#
# This script creates Ephemeral sequenced zodes
#
"""
Usage: create-with-acls.py [SECONDS]

	-h, --help		Show this help section
	SECONDS			How many seconds to stay running for?
					If this is not specified, a random value is used


"""


import logging
import random
import signal
import sys
import time

from docopt import docopt
from kazoo import security
from kazoo import exceptions

import core


#
# Delete a list of nodes
#
def delete_nodes(nodes):
	#
	# Sort the nodes in reverse order so that child nodes are
	# deleted before the parents
	#
	nodes = sorted(nodes)
	nodes.reverse()
	for node in nodes:
		zk.delete(node)


#
# Bails out when we get a signal
#
def signal_handler(signal, frame):
	logging.info("Ctrl-C received, deleting all nodes and then bailing out")
	delete_nodes(all_nodes)
	sys.exit(0)


#
# Check our command-line parameters
#
params = docopt(__doc__)
num_secs = 0
if (params["SECONDS"]):
	num_secs = int(params["SECONDS"])


#
# Our worker function to be run when a node is changed
#
def watch_node_worker(data, stat, node_to_watch):
	#print("watch_node(): data", data)
	if (data):
		logging.info("Change detected in node '%s': %s" % (node_to_watch, data) )
	else:
		logging.info("node '%s' was DELETED" % node_to_watch)

#
# All our nodes that we create
#
all_nodes = []

#
# Connect to Zookeeper and create some nodes of varying permissions
#
zk = core.connect()


#
# Create a node that we can read
#
acls = [
	security.make_acl("ip", "127.0.0.1",
		read = True, 
		)]
(key_full, key_local) = core.createKey(zk, acls)
all_nodes.append(key_full)
core.watch_node(zk, key_full, watch_node_worker)
#print zk.get_acls(key_full)
zk.get(key_full)


#
# Now create a node that is world:anyone with no permissions and see what happens
#
acls = [
	security.make_acl("world", "anyone",
		all = False
	)]
(key_full, key_local) = core.createKey(zk, acls)
all_nodes.append(key_full)
try:
	core.watch_node(zk, key_full, watch_node_worker)
except exceptions.NoAuthError as e:
	logging.info("Caught NoAuthError (as we should have)")
else:
	logging.warn("Expected an error, did not get one!")


#
# Finally, create a node that has a child under it.
# Then change the nodes permissions on the parent node and watch what happens
#
(key_full, key_local) = core.createKey(zk, ephemeral = False)
all_nodes.append(key_full)
core.watch_node(zk, key_full, watch_node_worker)

target_key = key_local + "/test_child-"
(child_key, child_key_local) = core.createKey(zk, ephemeral = False, target_key = target_key)
all_nodes.append(child_key)
core.watch_node(zk, child_key, watch_node_worker)

#
# Now change the parent node to read-only and try to delete the child
#
acls = [
	security.make_acl("world", "anyone",
		admin=True
	)]
zk.set_acls(key_full, acls)

try:
	zk.delete(child_key)
except exceptions.NoAuthError as e:
	logging.info("Caught NoAuthError (as we should have)")
else:
	logging.warn("Expected an error, did not get one!")

#
# Add delete ability back in so we can safely remove this node
#
acls = [
	security.make_acl("world", "anyone",
		delete=True, admin=True
	)]
zk.set_acls(key_full, acls)


#
# Sleep for a specific number of seconds
#
if (not num_secs):
	num_secs = random.randint(5, 60)

logging.info("Sleeping for %d seconds..." % num_secs)
signal.signal(signal.SIGINT, signal_handler)
time.sleep(num_secs)


logging.info("Woke up, deleting all nodes!")
delete_nodes(all_nodes)

