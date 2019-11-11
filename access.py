from flask import Flask
import pyodbc
import sqlalchemy
from sqlalchemy.sql import sqltypes as types

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