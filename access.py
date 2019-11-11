from flask import Flask
import pyodbc
import sqlalchemy
from sqlalchemy.sql import sqltypes as types

"""
Default Route ("/") - Go to a simple html template page that tells about your data.
GET ("/item") - Will return UP TO 1000 items from your data.
GET ("/item/<id>") - Will return a single item from your data, by ID. If you data does not have a unique identifier then please let me know and I will help you get one added.
DELETE("/item/<id>") - Will delete a single item (again, you will need a unique column name)
POST ("/item") - As opposed to GET, POST will create a new item in your database. The body of the request will contain the item to be added. 
"""

# Connect to server
server = 'imdbdata.database.windows.net'
database = 'imdbdata'
username = ''
password = ''
driver = '{ODBC Driver 17 for SQL Server}'

# Create Flask app
app = Flask(__name__)

# Routes
@app.route('/')

@app.route('/item', methods='GET')

@app.route('/item/<id>', methods='GET')

@app.route('/item/<id>', methods='DELETE')

@app.route('/item', methods='POST')
