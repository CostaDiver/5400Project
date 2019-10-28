# Arden Ott, Thomas Garza, Nate (James) Tanner
#
# A small function that is designed to take a IMDB data URL, download, unzip, and convert it to CSV.


import os
import requests
import gzip
import pandas as pd


def getcsv(url, csvname):
    # Gzipped TSV file
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

    # Close unneeded files
    os.remove('basics.tsv.gz')
    os.remove(f'{csvname}.tsv')


getcsv('https://datasets.imdbws.com/title.basics.tsv.gz', 'titlebasics')
getcsv('https://datasets.imdbws.com/title.ratings.tsv.gz', 'ratings')
