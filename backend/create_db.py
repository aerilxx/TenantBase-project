import sqlalchemy as db
from sqlalchemy import create_engine

def insert_data():
	# connect to DB
    engine = create_engine('sqlite:///database.db')
    conn = engine.connect()
    metadata = db.MetaData()

    # create tables
    emp = db.Table('emp', metadata,
	              db.Column('Name', db.String(255), nullable=False),
	              db.Column('Power', db.String(255))
	              )
    
    metadata.create_all(engine) 

	#Inserting many records at ones
    query = db.insert(emp) 
    values_list = [{'Name':'Bulbasaur', 'Power':'Poison'},
	               {'Name':'Charmeleon', 'Power':'Fire'},
	               {'Name':'Blastoise', 'Power':'Water'},
	               {'Name':'Metapod', 'Power':'Bug'},
	               {'Name':'Natu', 'Power':'Psychic'},
	               {'Name':'Pikachu', 'Power':'Electic'},
	               {'Name':'Sudowoodo', 'Power':'Rock'}]
    
    conn.execute(query,values_list)

insert_data()



