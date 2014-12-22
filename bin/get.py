#!/usr/bin/env python
#
# This script fetches info about all of the znodes
#


import logging
import signal
import sys
import time


import core


zk = core.connect()


#
# Grab our child nodes, sort them, and print them out
#
children = zk.get_children(core.key)
children = sorted(children)

for key in children:
	node = core.key + "/" + key
	data = zk.get(node)
	logging.info("Node: %s, Data: %s" % (node, data[0]))


