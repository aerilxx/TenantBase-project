#!/bin/bash


#install memcached
#sudo apt-get install memcached
#service memcached restart

# open memcached port 
#telnet localhost 11211

# run main program
python backend/main.py

python backend/memcache_like_server.py