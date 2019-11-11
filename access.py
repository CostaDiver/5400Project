"""
Arden Ott, Thomas Garza, Nate (James) Tanner

A Python script which creates a connection to our database from which we persisted data in the last assignment. Once
connected, we create a Flask app to allow the database to be accessed and edited over the internet. Data is returned
and entered in the JSON format. Movie lookups and row deletions are done using the tconst key value.
"""

from flask import Flask, request
import pyodbc


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
@app.route('/')  # Welcome screen describing the API
def welcome():
    desc = '''<br><h3>A small Flask app to return IMDB movie data. Available routes can be found below: </h3>
              <ul>
              <li>/item&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                Returns the top 1000 movies sorted by release year and rating. Can be used as a get or post 
                (using JSON) function.
                </li>
              <li>/item/id&nbsp;&nbsp;&nbsp;
                Returns a specific title where id is the tconst of the film. Can be used as a get or delete function.
                </li>
              </ul>'''
    return desc


@app.route('/item', methods=['GET'])  # Gets the top 1000 rows of our data sorted by year and rating descending
def return_1000():
    records = cursor.execute('''
    SELECT TOP 1000 Titles.tconst
                    ,primaryTitle
                    ,startYear
                    ,averageRating
                    ,numVotes
    FROM Ratings
        JOIN Titles
        ON Ratings.tconst = Titles.tconst
    WHERE isAdult = 0
    ORDER BY startYear DESC
             ,averageRating DESC
    FOR JSON AUTO''').fetchone()

    cursor.close()
    return records[0]


@app.route('/item/<id>', methods=['GET'])  # Gets a specific movie by searching the tconst
def return_one(id):
    records = cursor.execute('''
    SELECT Titles.tconst
           ,primaryTitle
           ,startYear
           ,averageRating
           ,numVotes
    FROM Ratings
        JOIN Titles
        ON Ratings.tconst = Titles.tconst
    WHERE isAdult = 0 AND Titles.tconst = (?)
    ORDER BY startYear DESC
             ,averageRating DESC
    FOR JSON AUTO;''', id).fetchone()

    cursor.close()
    return records[0]


@app.route('/item/<id>', methods=['DELETE'])  # Allows for the deleting of a movie by entering the tconst
def delete_one(id):
    try:
        cursor.execute('''DELETE FROM Ratings WHERE Ratings.tconst = (?);''', id)
        cursor.execute('''DELETE FROM Titles WHERE Titles.tconst = (?);''', id)
        conn.commit()
        return f'{id} deleted from Ratings and Titles tables.'
    except:
        return 'Delete Failed.'


@app.route('/item', methods=['POST'])  # Allows a new row to be entered with data in JSON format
def post_one():
    """
    To test this function, use this JSON data as the input:

    {
        "tconst":"tt10914342",
        "titleType":"movie",
        "primaryTitle":"Kirket",
        "originalTitle":"Kirket",
        "isAdult":"0",
        "startYear":2019,
        "endYear":"",
        "runtimeMinutes":"132",
        "genres":"Drama,Sport",
        "Ratings":
            [{"averageRating":10,
            "numVotes":580}]
    }

    """

    data = request.get_json()

    # Declare column values
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

    # Don't run if the tconst is already found in the database
    if len(cursor.execute('SELECT COUNT(*) FROM Titles WHERE Titles.tconst = (?)', tconst).fetchall()) > 0:
        return f'Record with tconst {tconst} already exists in DB'

    try:
        cursor.execute(query_titles, tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear,
                       runtimeMinutes, genres)
        cursor.execute(query_ratings, tconst, averageRating, numVotes)

        conn.commit()
        return 'Record inserted.'
    except:
        return 'Record not inserted.'


if __name__ == '__main__':
    app.run()
