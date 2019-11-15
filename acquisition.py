"""
Arden Ott, Thomas Garza, Nate (James) Tanner

A small function that is designed to take a IMDB data URL, download, unzip, and convert it to CSV.
One file contains every single item on IMDB, and basic info about it. The other file contains the user ratings for
all of those items. The data is quite large, combined it works out to a little over half a GB. Part of this issue
is that we only need movies, but the data includes short films, video games, and other non-movie datapoints. Stripping
the file of those rows shrinks it to about 45 MB.

The data seems pretty clean, so it doesn't look like we will need to do any major scrubbing aside from filtering
out unneeded lines and including NULL values.
"""


from os import remove
from requests import get
from gzip import GzipFile
from pandas import read_table
from csv import reader, writer


def getcsv(url, csvname):
    # Gets Gzipped TSV file
    print('Downloading file... \n')
    r = get(url)
    open('basics.tsv.gz', 'wb').write(r.content)

    # Unzips into a TSV file
    print('Unzipping file...\n')
    basics = GzipFile('basics.tsv.gz', 'rb')
    s = basics.read()
    basics.close()
    output = open(f'{csvname}.tsv', 'wb')
    output.write(s)
    output.close()

    # Define column datatypes
    datatypes = dict()
    if csvname == 'titlebasics':
        datatypes = {'tconst': str, 'titleType': str, 'primaryTitle': str, 'originalTitle': str, 'isAdult': str,
                     'startYear': str, 'endYear': str, 'runtimeMinutes': str, 'genres': str}
    elif csvname == 'ratings':
        datatypes = {'tconst': str, 'averageRating': float, 'numVotes': int}

    # Converts to CSV file
    print('Converting to CSV...\n')
    tsv_file = f'{csvname}.tsv'
    csv_table = read_table(tsv_file, sep='\t', dtype=datatypes)
    csv_table.to_csv(f'{csvname}.csv', index=False,)

    # Remove all rows except for movies
    print('Deleting non-movie lines...\n')
    inp = open(f'{csvname}.csv', 'r', encoding='UTF-8', errors='ignore')
    out = open(f'{csvname}_edit.csv', 'w', newline='')
    csvwriter = writer(out)

    if csvname == 'titlebasics':  # This only runs on the titlebasics dataset
        first_line = True
        for row in reader(inp):
            while '\\N' in row:  # Replace \N values with nothing
                location = row.index('\\N')
                row[location] = ''
            if first_line:  # Always write first line
                first_line = False
                csvwriter.writerow(row)
            elif row[1] == 'movie':  # Write lines that include movie as the title type
                csvwriter.writerow(row)

    elif csvname == 'ratings':  # This only runs on the ratings dataset
        # Open TitleBasics and write all Tconst values to a set so that it can be easily searched
        titlebasics = open('titlebasics_edit.csv', 'r', encoding='UTF-8', errors='ignore')
        tconst = set()
        for row in reader(titlebasics):
            tconst.add(row[0])

        first_line = True
        for row in reader(inp):
            while '\\N' in row:  # Replace \N values with nothing
                location = row.index('\\N')
                row[location] = ''
            if first_line:  # Always write first line
                first_line = False
                csvwriter.writerow(row)
            elif row[0] in tconst:  # Only write lines that have a matching tconst
                csvwriter.writerow(row)

    # Delete unneeded files
    inp.close()
    out.close()
    remove('basics.tsv.gz')
    remove(f'{csvname}.tsv')
    remove(f'{csvname}.csv')


# Basics file contains all movies and basic info like title, year released, etc.
getcsv('https://datasets.imdbws.com/title.basics.tsv.gz', 'titlebasics')
# Contains ratings for all movies.
getcsv('https://datasets.imdbws.com/title.ratings.tsv.gz', 'ratings')
