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


