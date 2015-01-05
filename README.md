# Zookeeper-Demo

Zookeeper is a filesystem. Sort of.  It is also a database. Sort of.

Zookeeper allows you to store data that distributed, highly available, and highly consistent, even when some Zookeeper servers are unavailable. Common uses of Zookeeper include storage of configuration information, naming, providing distributed synchronization, and providing group services.

In an effort to learn Zookeeper, I put together a collection of scripts that talk to a virtual cluster of Zookeeper instances.  These scripts do reading, writing, and advanced features such as watching and master/leader election.


## Quickstart

Make sure you have Vagrant installed: [https://www.vagrantup.com/](https://www.vagrantup.com/)

To spin up 3 viritual machines, clone this repo and type: `vagant up zoo1 zoo2 zoo3`.  This will spin up (and provision) a cluster of 3 VMs each running Zookeeper.  Each instance uses 256 MB of RAM, for 3/4ths of a Gig total usage.

The provisioning process on each instance consists of the following:

- Running `apt-get update`
- Installing Zookeeper and Python Setuptools
- Installing pip, the Python package manager
- Installing the modules required by our Python code including [Kazoo](https://kazoo.readthedocs.org/en/latest/)
- Installing configuration files and server IDs for each Zookeeper server
- Restarting the Zookeeper server

### Accessing the Zookeeper servers

You can SSH into each server by typing `vagrant ssh zoo1` (or zoo2 or zoo3 as appropriate).  Once SSHed into a server, each server has an internal IP as follows:

- zoo1: 10.0.10.101
- zoo2: 10.0.10.102
- zoo3: 10.0.10.103



## Utilities to play with

I've written the following Python scripts which let you play with Zookeeper

- `watch.py` - Watches the /zkdemo znode in Zookeeper until the script is terminated with ^C.  All nodes that these scripts create are written there.  When a node is created, updated, or deleted, this script prints that out.  It's a good idea to leave this script running in one terminal while you run…
- `create.py [NUMBER]` - Creates a single Znode under /zkdemo. The znode is ephemeral (it is deleted when the client disconnects) and seqeuntial (it receives a unique auto incrementing number, not unlike what MySQL does)  If an argument is specified, that is the number of seconds that this script stays running (and keeping the ephemeral node alive) before existing.  If NUMBER is not specified, the script runs for a random number of seconds between 1 and 60.
    - Another use of this script is that it will check to see if multiple Znodes in that directory exist, and perform rudimentary master/leader election as outlined by the algorithm at [http://zookeeper.apache.org/doc/trunk/recipes.html#sc_leaderElection](http://zookeeper.apache.org/doc/trunk/recipes.html#sc_leaderElection)
- `get.py` - Lists all znodes under /zkdemo and then exits.  This script (in addition to `watch.py`) is useful when running
- `create-start.py NUMBER` - Run this script with an integer argment, and the same number of processes which cause `create.py` to be run in an endless loop will run.  Since `create.py` has a random timeout by default, this can be used to watch master election in action.
- `create-stop.py` - Stop all of the scripts created by `create-start.py`
- `acl-lockdown.py` - Lock down Zookeeper by making / read-only to everyone, except for 127.0.0.1, which has full access.
    - Try running this script pointed directly at a server's IP (such as 10.0.10.101) and you'll see it fail with a NoAuth exception.
- `create-with-acls.py` - Test out some node creation/deletion operations with ACLs based on IP addresses

All of the above scripts except for `create-start.py` take the optional argument `--host=IP[,IP[,IP[,…]]]` to specify specific IP addresses to connect to.  Kazoo will pick a random IP address from that list to try connecting to.  Zookeeper runs on port 2181, but there's no need to specifty the port number with `--hosts` as it is the default, and used when no port number is specified.  

Assuming that the cluster is in working order, anything written to one node will be immediately readable by any other node, as Zookeeper is highly consistent.


## Getting up close and personal with Zookeeper

### The CLI

The CLI can be run by typing `/usr/share/zookeeper/bin/zkCli.sh` while on the command line of one of the virutal machines.

The `ls /` and `ls /zkdemo` commands are getting starting points.  `create`, `get`, and `delete` are also worth trying if you'd like to play around in Zookeeper and create your own znodes.

Remember, anything written on one node will immediately be available on the other nodes, so it won't matter which machine you've SSHed into.


### Logfiles and troubleshooting
 
A good place to start looking for errors is `/var/log/zookeeper/zookeeper.log`.  It helps to ignore all lines that have "INFO" as the facility (and believe me, there will be many of those).  Pay attention to the WARN and ERROR lines instead.



## Bugs

I could never figure out how to get digest auth to work. (usernames and passwords)  Any advice is appreciated!


## For Further Reading

- [The Kazoo Documentation](https://kazoo.readthedocs.org/en/latest/)
- [Apache Zookeeper Official Page](http://zookeeper.apache.org/)
- [Zookeeper Internals](http://zookeeper.apache.org/doc/r3.4.1/zookeeperInternals.html)
- [Call me maybe: Zookeeper](https://aphyr.com/posts/291-call-me-maybe-zookeeper)
- [Apache Zookeeper: How do writes work?](http://stackoverflow.com/questions/5420087/apache-zookeeper-how-do-writes-work)
- [How-to: Use Apache ZooKeeper to Build Distributed Apps (and Why)](http://blog.cloudera.com/blog/2013/02/how-to-use-apache-zookeeper-to-build-distributed-apps-and-why/)


## Contact

I can be reach via email (dmuth@dmuth.org) or [various forms of social media](http://www.dmuth.org/contact)








