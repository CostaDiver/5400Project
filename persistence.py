"""
Nate Tanner, Arden Ott, Thomas Garza

1) We will be using an Azure SQL Server Database, imdbdata.database.windows.com
2) See question 1.
3) We chose it because it allowed all of us to have good accessibility to the DB, learn something new, and familiarize
    ourselves with cloud hosted database services. We chose SQL Server because its what we use in the Hunstman School
     database courses so we all have familiarity with it.

 1) The database is set up on Azure at imdbdata.database.com. UID = python, PASS = MIS5400!
 2) See below script.
 3) Our DB will be relational, it has two tables; one for titles and information, another for ratings. They are related
    through a T_Const key value.
    CREATE TABLE Titles(
        tconst varchar(10) NOT NULL,
        titleType varchar(25),
        primaryTitle varchar(max),
        isAdult int,
        StartYear int,
        endYear int,
        runtimeMinutes int,
        genres varchar(max),
        PRIMARY KEY(tconst)
    );

    CREATE TABLE Ratings(
        tconst varchar(10) NOT NULL,
        averageRating decimal(2,1),
        numVotes int
        PRIMARY KEY(tconst)
    );
"""

import pyodbc
import pandas as pd
from urllib import parse as url
import sqlalchemy
from sqlalchemy.sql import sqltypes as types

server = 'imdbdata.database.windows.net'
database = 'imdbdata'
username = 'ntanner'
password = 'JNTdiver1776!'
driver = '{ODBC Driver 17 for SQL Server}'

# write to sql table... pandas will use default column names and dtypes
params = url.quote_plus(f'DRIVER={driver};PORT=1433;SERVER={server};DATABASE={database};UID={username};PWD={password}')

# set up connection to database (with username/pw if needed)
print('Converting CSVs to Datafiles...')
ratings_df = pd.read_csv(r'ratings_edit.csv', quotechar='"', low_memory=False)
titles_df = pd.read_csv(r'titlebasics_edit.csv', quotechar='"', low_memory=False)

print('Connecting to DB...')
engine = sqlalchemy.create_engine(f"mssql+pyodbc:///?odbc_connect=%s" % params)

print('Uploading titles DF to DB...')
# tconst,titleType,primaryTitle,originalTitle,isAdult,startYear,endYear,runtimeMinutes,genres
titles_dtypes = {'tconst': types.VARCHAR(), 'titleType': types.VARCHAR(), 'primaryTitle': types.VARCHAR(),
                 'originalTitle': types.VARCHAR(), 'isAdult': types.INT(), 'startYear': types.INT(), 'endYear': types.INT(),
                 'runtimeMinutes': types.INT(), 'genres': types.VARCHAR()}
titles_df.to_sql("Titles", engine, if_exists='replace', index=False, chunksize=100, method='multi', dtype=titles_dtypes)

print('Uploading ratings DF to DB...')
# tconst,averageRating,numVotes
ratings_dtypes = {'tconst': types.VARCHAR(), 'averageRating': types.INT(), 'numVotes': types.INT()}
ratings_df.to_sql("Ratings", engine, if_exists='replace', index=False, chunksize=200, method='multi', dtype=ratings_dtypes)
