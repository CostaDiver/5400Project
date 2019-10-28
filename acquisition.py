import requests
import gzip


with gzip.open(requests.get('https://datasets.imdbws.com/title.basics.tsv.gz')) as f:
    titles_content = f.read()


with gzip.open(requests.get('https://datasets.imdbws.com/title.ratings.tsv.gz')) as f:
    ratings_content = f.read()


