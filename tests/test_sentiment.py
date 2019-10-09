import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gzip
import csv
import config
import psycopg2
from textblob import TextBlob

PATH = "/home/ed/Documents/reviewanalyzer/tests/split_test/"
FILE_NAME = "{}sample_us.tsv.gz".format(PATH)


def read_file():
    line = 0
    conn = psycopg2.connect(**config.postgres_db)
    conn.autocommit = True
    with gzip.open(filename=FILE_NAME, mode="rt") as g:
        reader = csv.reader(g, delimiter="\t")
        header = next(reader)
        print(header)
        insert_list = list()
        for row in reader:
            body = row[13]
            blob = TextBlob(body)
            insert_list.append((row[5], row[7], row[12], body, blob.sentiment[0]*100))
            if len(insert_list) > 9000:
                insert_results(conn, insert_list)
                insert_list = list()
            line += 1
        if len(insert_list) > 0:
            insert_results(conn, insert_list)

    conn.close()


def insert_results(conn, res_list):
    cur = conn.cursor()

    insert_stmt = '''
        insert into analysis.review_sentiment2
        (product_title, star_rating, review_headline, review_body, sentiment)
        VALUES (%s, %s, %s, %s, %s)
    '''
    cur.executemany(insert_stmt, res_list)
    cur.close()

if __name__ == "__main__":
    read_file()
