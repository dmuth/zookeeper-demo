#!/usr/bin/env python
#
# This script watches a specific zode and prints up changes to it
#


import logging
import time


import core


zk = core.connect()


@zk.ChildrenWatch(core.key)
def watch_children(children):
    logging.info("Children of %s are now: %s" % (core.key, children) )

logging.info("Watching %s for changes. Press ^C to abort..." % core.key)

#
# Loop forever, just printing up node changes when we get them
#
while 1:
	time.sleep(3600)


