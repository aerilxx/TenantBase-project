# TenantBase-project
Interview project for tenantbase

### Installation:

```
# set virtual environment and install package
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# run bash file to set up memcached in background and instatiate to DB
bash run.sh
```

* http://127.0.0.1:8000 to view initial data in db
* http://127.0.0.1:8000/add to manipulate db in browser, new data will be automatically cached in memcached

```
# run memcache-like-server on another port bc 11211 is taken in flask 
python backend/memcache_like_server.py

# connect to this server in another cmd
telnet 120.0.0.1 110210
```
You can perform set/get/delete function 
