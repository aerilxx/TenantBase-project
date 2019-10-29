# TenantBase-project
Interview project for tenantbase

### Installation:

```
# set virtual environment and install package
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
# instantiate db for display (once)
cd backend
python create_db.py
# run bash file to set up memcached in background and run main flask as well as new server
bash backend/run.sh
```

* http://127.0.0.1:5000 to view initial data in db
* http://127.0.0.1:5000/add to manipulate db in browser, new data will be automatically cached in memcached
* http://127.0.0.1:5000/display to display server data

You can perform set/get/delete function using telnet 127.0.0.1 11210
