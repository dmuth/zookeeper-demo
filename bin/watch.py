#!/usr/bin/env python
#
# This script watches a specific zode and prints up changes to it
#


import logging
import signal
import sys
import time


import core


#
# Bails out when we get a signal
#
def signal_handler(signal, frame):
	logging.info("Ctrl-C received. Deleting key")
	zk.delete(key)
	sys.exit(0)

zk = core.connect()


@zk.ChildrenWatch(core.key)
def watch_children(children):
    logging.info("Children of %s are now: %s" % (core.key, children) )

logging.info("Watching %s for changes. Press ^C to abort..." % core.key)

#
# Wait for the user to press ctrl-C
#
signal.signal(signal.SIGINT, signal_handler)
signal.pause()


