#!/bin/bash

# if you don't have existing db to display on index, instatiate 
python backend/create_db.py

#install memcached
sudo apt-get install memcached
service memcached restart

# open memcached port 
telnect localhost 11211

# run main program
python backend/main.py