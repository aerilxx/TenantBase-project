from flask import Flask, render_template, request,flash, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData, Table, select
import sys
import memcache

app = Flask(__name__)
app.secret_key ="secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# set up memcache client
client = memcache.Client([('localhost', 11211)])

# database related func
def fetchData():
    engine = db.create_engine('sqlite:///database.db',{})
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('emp', metadata, autoload=True, autoload_with=engine)
    cmd = db.select([table])
    resultProxy = connection.execute(cmd)
    resultSet = resultProxy.fetchall()

    return resultSet

def query_db(pokemon):
    res = ''
    engine = db.create_engine('sqlite:///database.db',{})
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('emp', metadata, autoload=True, autoload_with=engine)
    try:
        select_st2 = table.select().where(table.c.Name == '{}'.format(pokemon))
        result = connection.execute(select_st2)
        
        for _row in result:
            res = _row[1]
    except Exception as e:
        res = "invalid"
        print(e)
    
    return res

def add_db(pokemon, power):
    msg = ""
    engine = db.create_engine('sqlite:///database.db',{})
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('emp', metadata, autoload=True, autoload_with=engine)
    #Inserting record one by one
    try:
        query = db.insert(table)
        item = [{'Name': '{}'.format(pokemon), 'Power': '{}'.format(power)}]
        
        if_exist = table.select().where(table.c.Name == '{}'.format(pokemon))
        result = connection.execute(if_exist)
        if pokemon == result:
            msg = "You cannot add duplicate pokemon in db."
        else:
            connection.execute(query,item)  
            msg = "add {} successfully!".format(pokemon)
            
    except SQLAlchemyError as e:
        msg = e
     
    return msg


@app.route('/')
def index():
    data = fetchData('')
    return render_template('index.html', pokemons = data)


@app.route('/add' , methods=['GET','POST'])
def display_form():
    return render_template('tcp.html')

@app.route('/searchPokemon', methods = ['GET'])
def showdata():    

# first form
    if request.method == "GET":
        search_pokemon = request.values['searchname']
        msg = ""

        if search_pokemon is "":
            msg = "hey you can't search nothing !"
        else:
            # first see if this key value in memcached
            search_result = client.get(search_pokemon)     
            result = ""

            if search_result is None:
                result = query_db(search_pokemon)
                
                if result == 'invalid':
                    msg = "We don't have this pokemon in database!! You can add it!"
                # if the data not in cache but in database
                else:
                    msg = "Seems like this pokemon is in database. Let's save it in memcached so someone can get it sooner! => pokemon : {p}, power: {d}".format(p=search_pokemon, d=result)
                    client.set(search_pokemon, result)
                    
            else:
                # data already in memcached
                mem_result = client.get(search_pokemon)
                print(mem_result)
                msg = "got the data directly from memcache! => {p} has {d} power!".format(p=search_pokemon, d=mem_result)
            
        flash(msg)

# second form, add pokemon and power to database

    add_pokemon = request.values['addname']
    add_power = request.values['addpower']

    msg2 = ''
    if add_pokemon is '' or add_power is '':
        msg2 = "please submit a valid pokemon and power."
    else:
        mem_result = client.get(add_pokemon)   

        if mem_result is None:
            db_result = query_db(add_pokemon)
            
            if db_result == 'invalid':
                info = add_db(add_pokemon, add_power)
                msg = "We don't have this pokemon in database!! You can add it! "+info

            # if the data not in cache but in database
            else:
                msg = "Seems like this pokemon is in database."
                    
        else:
            # data already in memcached
            msg = "This pokemon already exists from memcache! => {p} has {d} power!".format(p=add_pokemon, d=mem_result)
        




    return render_template('tcp.html')

   

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
