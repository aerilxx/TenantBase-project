from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


def fetchData():
    engine = db.create_engine('sqlite:///database.db',{})
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('emp', metadata, autoload=True, autoload_with=engine)
    query = db.select([table])
    resultProxy = connection.execute(query)
    resultSet = resultProxy.fetchall()
    return resultSet

@app.route('/')
def index():
    data = fetchData()
    print(data)
    return render_template('index.html', pokemons = data)


    
   

if __name__ == '__main__':
    app.run(port = 8000, debug=True)
