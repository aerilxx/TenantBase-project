#!/bin/bash

#install memcached
#sudo apt-get install memcached
#service memcached restart

# open memcached port 
#telnet localhost 11211

# run main program
python memcache_like_server.py &
python main.py
