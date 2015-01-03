#!/usr/bin/env python
#
# This script watches a specific zode and prints up changes to it
#


import logging
import signal
import sys
import time

from kazoo import exceptions

import core


#
# Bails out when we get a signal
#
def signal_handler(signal, frame):
	sys.exit(0)

zk = core.connect()


@zk.ChildrenWatch(core.key)
def watch_children(children):
	logging.info("Children of %s are now: %s" % (core.key, children) )
	children = sorted(children)
	for child in children:
		node = core.key + "/" + child

		try:
			data = zk.get(node)
			logging.info("Node: %s, Data: %s" % (child, data[0]))

		except exceptions.NoAuthError as e:
			logging.info("Node '%s' was denied access" % (child) )

		except exceptions.NoNodeError as e:
			logging.info("Node '%s' was deleted" % (child) )

logging.info("Watching %s for changes. Press ^C to abort..." % core.key)

#
# Wait for the user to press ctrl-C
#
signal.signal(signal.SIGINT, signal_handler)
signal.pause()


