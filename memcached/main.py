from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    data = fetchData()
    print(data)
    return render_template('index.html', pokemons = data)


if __name__ == '__main__':
    app.run(debug=True)
