#
# This module is imported and sets common settings
#

import commands

import coloredlogs, logging
coloredlogs.install()
logging.basicConfig(level=logging.INFO)


from kazoo.client import KazooClient
from kazoo.client import KazooState

#
# This is the main znode that we'll be working with in this demo
#
key = "/zkdemo"


#
# Connect to Zookeeper and return the handle.
#
def connect():
	retval = KazooClient(hosts='127.0.0.1:2181')

	def my_listener(state):
		if state == KazooState.LOST:
			# Register somewhere that the session was lost
			logging.warn("Lost connection to Zookeeper")

		elif state == KazooState.SUSPENDED:
			# Handle being disconnected from Zookeeper
			logging.warn("Zookeeper connection suspended")

		elif state == KazooState.CONNECTED:
			pass

		else:
			# Handle being connected/reconnected to Zookeeper
			logging.info("Other state: %s" % state)

	retval.add_listener(my_listener)
	retval.start()

	if not retval.exists(key):
		logging.info("Created '%s'" % key)
		retval.create(key)

	return(retval)

#
# This function can be used as a decorator to provide static variables 
# for functions.
#
# Borrowed from http://stackoverflow.com/a/279586/196073
#
def static_var(varname, value):
	def decorate(func):
		setattr(func, varname, value)
		return func
	return decorate


#
# Return the current IP address
#
def getIP():
	retval = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
	return(retval)



#
#
# @param object zk The Zookeeper object
# @param string node_to_watch The name of the znode to watch for changes
# @param function cb The callback to fire when this znode changes.
#
# This function sets up a watch on a Node.
# Because a watcher function is called when it is assigned and an 
# unlimited number of times when a node changes (or is deleted), 
# we need to have a little wrapper which ensures that a specific 
# node can only be watched ONCE.
#
@static_var("watched", {})
def watchNode(zk, node_to_watch, cb):

	if node_to_watch in watchNode.watched:
		return False
	
	watchNode.watched = node_to_watch
	logging.info("Watching key: %s" % node_to_watch)

	@zk.DataWatch(node_to_watch)
	def watch_node(data, stat):
		cb(data, stat, node_to_watch)


#
#
# @param object zk The Zookeeper object
# @param string our_key The name of our znode
# @param object cb The callback to figre when the ndoe changes--this is 
#	passed back into a call to watchNode().
#
# Get our children and determine if we are the master (first) node.
# If not, watch the node immediately before this one.
#
def isMasterNode(zk, our_key, cb):

	children = zk.get_children(key)
	children = sorted(children)

	if (children[0] == our_key):
		logging.info("We're the master node!")

	else:
		last_node = ""
		for child in children:
			if (child == our_key):
				node_to_watch = key + "/" + last_node
				logging.info("Found our key, watching the previous key (%s)" % node_to_watch)
				watchNode(zk, node_to_watch, cb)
				break

			last_node = child


