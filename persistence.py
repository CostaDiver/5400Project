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
"""

import pyodbc
import pandas as pd
import sqlalchemy

server = 'imdbdata.database.windows.net'
database = 'imdbdata'
username = 'python'
password = 'MIS5400!'
driver = '{ODBC Driver 17 for SQL Server}'
conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()

# set up connection to database (with username/pw if needed)
# read csv data to dataframe with pandas
# datatypes will be assumed
# pandas is smart but you can specify datatypes with the `dtype` parameter
#df = pd.read_csv(r'ratings.csv')
#df1 = pd.read_csv(r'titlebasics.csv')

# write to sql table... pandas will use default column names and dtypes
#df.to_sql('table_name',engine,index=True,index_label='id')
#df.to_sql()