#!/usr/bin/env python
#
# This script fetches info about all of the znodes
#
"""
Usage: get.py [--host=<hostname>]

	--host=<hostname>	The hostname and port to connect to [default: 127.0.0.1:2181]

This script will lock down / in your Zookeeper installation so that only 
127.0.0.1 can create new znodes


"""


import logging
import signal
import sys
import time

from docopt import docopt

import core

params = docopt(__doc__)
if not params["--host"]:
	params["--host"] = "127.0.0.1:2181"

zk = core.connect(params["--host"])


#
# Grab our child nodes, sort them, and print them out
#
children = zk.get_children(core.key)
children = sorted(children)

for key in children:
	node = core.key + "/" + key
	data = zk.get(node)
	logging.info("Node: %s, Data: %s" % (node, data[0]))


