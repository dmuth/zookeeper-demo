#!/usr/bin/env python


import logging
import time


import core


zk = core.connect()


if not zk.exists(core.key):
	logging.info("Created '%s'" % core.key)
	zk.create(core.key)

@zk.ChildrenWatch(core.key)
def watch_children(children):
    logging.info("Children of %s are now: %s" % (core.key, children) )

zk.create(core.key + "/testseq-", ephemeral=True, sequence=True)

logging.info("Watching %s for changes. Press ^C to abort..." % core.key)

#
# Loop forever, just printing up node changes when we get them
#
while 1:
	time.sleep(3600)


