# Arden Ott, Thomas Garza, Nate (James) Tanner
#
# A small function that is designed to take a IMDB data URL, download, unzip, and convert it to CSV.
# One file contains every single item on IMDB, and basic info about it. The other file contains the user ratings for
# all of those items. The data is quite large, combined it works out to a little over half a GB. Part of this issue
# is that we only need movies, but the data includes short films, video games, and other non-movie datapoints. Stripping
# those datapoints will be done in the next part of the project.
#
# The data seems pretty clean, so it doesn't look like we will need to do any major scrubbing aside from filtering
# out unneeded lines.


import os
import requests
import gzip
import pandas as pd
import csv


def getcsv(url, csvname):
    # Gets Gzipped TSV file
    print('Downloading file... \n')
    r = requests.get(url)
    open('basics.tsv.gz', 'wb').write(r.content)

    # Unzips into a TSV file
    print('Unzipping file...\n')
    basics = gzip.GzipFile('basics.tsv.gz', 'rb')
    s = basics.read()
    basics.close()
    output = open(f'{csvname}.tsv', 'wb')
    output.write(s)
    output.close()

    # Converts to CSV file
    print('Converting to CSV...\n')
    tsv_file = f'{csvname}.tsv'
    csv_table = pd.read_table(tsv_file, sep='\t', low_memory=False)
    csv_table.to_csv(f'{csvname}.csv', index=False,)

    # Remove all rows except for movies
    print('Deleting non-movie lines...')
    inp = open(f'{csvname}.csv', 'r')
    out = open(f'{csvname}_edit.csv', 'w')
    writer = csv.writer(out)

    if csvname == 'titlebasics':
        first_line = True
        for row in csv.reader(inp):
            while '\\N' in row:
                location = row.index('\\N')
                row[location] = ''
            if first_line:
                first_line = False
                writer.writerow(row)
            elif row[1] == 'movie':

                writer.writerow(row)
    elif csvname == 'ratings':
        titlebasics = open('titlebasics_edit.csv')
        tconst = set()

        for row in csv.reader(titlebasics):
            tconst.add(row[0])
        first_line = True
        for row in csv.reader(inp):
            while '\\N' in row:
                location = row.index('\\N')
                row[location] = ''
            if first_line:
                first_line = False
                writer.writerow(row)
            elif row[0] in tconst:
                writer.writerow(row)

    # Delete unneeded files
    os.remove('basics.tsv.gz')
    os.remove(f'{csvname}.tsv')
    os.remove(f'{csvname}.csv')


# Basics file contains all movies and basic info like title, year released, etc.
getcsv('https://datasets.imdbws.com/title.basics.tsv.gz', 'titlebasics')
# Contains ratings for all movies.
getcsv('https://datasets.imdbws.com/title.ratings.tsv.gz', 'ratings')
