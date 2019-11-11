from flask import Flask, request
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
username = 'python'
password = 'MIS5400!'
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER=' + driver + f';SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()
# Create Flask app
app = Flask(__name__)


# Routes
@app.route('/')
def welcome():
    desc = '''A small function that is designed to take a IMDB data URL, download, unzip, and convert it to CSV.'
desOne file contains every single item on IMDB, and basic info about it. The other file contains the user ratings for
all of those items. The data is quite large, combined it works out to a little over half a GB. Part of this issue
is that we only need movies, but the data includes short films, video games, and other non-movie datapoints. Stripping
the file of those rows shrinks it to about 45 MB.'''
    return desc


@app.route('/item', methods=['GET'])
def return_1000():
    records = cursor.execute('''SELECT TOP 1000 Titles.tconst, primaryTitle, startYear, averageRating, numVotes
    FROM Ratings
    JOIN Titles
    ON Ratings.tconst = Titles.tconst
    WHERE isAdult = 0
    ORDER BY startYear DESC, averageRating desc
    FOR JSON AUTO''').fetchone()

    cursor.close()
    return records[0]


@app.route('/item/<id>', methods=['GET'])
def return_one(id):
    records = cursor.execute('''SELECT Titles.tconst, primaryTitle, startYear, averageRating, numVotes
    FROM Ratings
    JOIN Titles
    ON Ratings.tconst = Titles.tconst
    WHERE isAdult = 0 AND Titles.tconst = (?)
    ORDER BY startYear DESC, averageRating desc
    FOR JSON AUTO;''', id).fetchone()

    cursor.close()
    return records[0]


@app.route('/item/<id>', methods=['DELETE'])
def delete_one(id):
    try:
        cursor.execute('''DELETE FROM Ratings WHERE Ratings.tconst = (?);''', id)
        cursor.execute('''DELETE FROM Titles WHERE Titles.tconst = (?);''', id)
        conn.commit()
        return f'{id} deleted from Ratings and Titles tables.'
    except:
        return 'Delete Failed.'


@app.route('/item', methods=['POST'])
def post_one():
    data = request.get_json()

    tconst = data['tconst']
    titleType = data['titleType']
    primaryTitle = data['primaryTitle']
    originalTitle = data['originalTitle']
    isAdult = data['isAdult']
    endYear = data['endYear']
    runtimeMinutes = data['runtimeMinutes']
    genres = data['genres']
    startYear = data['startYear']
    averageRating = data['Ratings'][0]['averageRating']
    numVotes = data['Ratings'][0]['numVotes']

    query_titles = 'INSERT INTO Titles VALUES(?,?,?,?,?,?,?,?,?)'
    query_ratings = 'INSERT INTO Ratings VALUES(?, ?, ?)'

    if len(cursor.execute('SELECT COUNT(*) FROM Titles WHERE Titles.tconst = (?)', tconst).fetchall()) > 0:
        return f'Record with tconst {tconst} already exists in DB'

    try:
        cursor.execute(query_titles, tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear,
                       runtimeMinutes, genres)
        cursor.execute(query_ratings, tconst, averageRating, numVotes)

        conn.commit()
        return 'Record inserted.'
    except:
        return 'Not inserted'


if __name__ == '__main__':
    app.run()

# [{"tconst":"tt10914342","titleType":"movie","primaryTitle":"Kirket","originalTitle":"Kirket","isAdult":"0","startYear":2019, "endYear":"","runtimeMinutes":"132","genres":"Drama,Sport","Ratings":[{"averageRating":10,"numVotes":580}]}]

# tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres
# tt10914342	movie	Kirket	Kirket	0	2019		132	Drama,Sport

# tconst	averageRating	numVotes
# tt10914342	10	583
