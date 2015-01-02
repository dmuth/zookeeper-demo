#!/usr/bin/env python
#
# This script lets me play around with ACLs on the Zookeeper installation
#
"""
Usage: acl-lockdown.py [--host=<hostname>]

	--host=<hostname>	The hostname and port to connect to [default: 127.0.0.1:2181]

This script will lock down / in your Zookeeper installation so that only 
127.0.0.1 can create new znodes


"""


import logging
import random
import signal
import sys
import time

from docopt import docopt
from kazoo import security


import core


params = docopt(__doc__)
host = params["--host"]
if not host:
	host = "127.0.0.1:2181"

zk = core.connect(host)


#
# Change / to be readable by everyone, and writeable only by localhost.
#
acls = [
	security.make_acl("world", "anyone",
		read = True,
	),
	security.make_acl("ip", "127.0.0.1",
		all = True
	),
	]
zk.set_acls("/", acls)

logging.info("/ has been changed to read-only for everyone but localhost")


