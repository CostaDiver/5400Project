import flask
import pyodbc
import sqlalchemy
from sqlalchemy.sql import sqltypes as types

server = 'imdbdata.database.windows.net'
database = 'imdbdata'
username = ''
password = ''
driver = '{ODBC Driver 17 for SQL Server}'

@app.route('/')

@app.get('/item')

@app.get('/item/<id>')

@app.delete('/item/<id>')

@app.post('/item')