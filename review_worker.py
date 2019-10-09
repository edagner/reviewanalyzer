import multiprocessing
import boto3
import io
import gzip
import csv
import psycopg2
import config
from textblob import TextBlob
from review_poller import sqs, QUEUE_URL
try:
    from aws_config import ACCESS_ID, ACCESS_KEY
except ImportError:
    ACCESS_ID, ACCESS_KEY = None, None


s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_ID,
    aws_secret_access_key=ACCESS_KEY,
    region_name='us-east-2')


class Worker(multiprocessing.Process):
    def __init__(self, work):
        super(Worker, self).__init__()
        self.work = work

    def run(self):
        print(self.work)
        # connect to S3 and read review line by line, grading each review
        s3_read(self.work[0])
        # Delete received message from queue
        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=self.work[1])


def s3_read(file_name):
    line = 0
    obj = s3.Object(bucket_name='reviews-ingestion', key=file_name)
    buffer = io.BytesIO(obj.get()["Body"].read())
    insert_list = list()

    conn = psycopg2.connect(**config.postgres_db)
    conn.autocommit = True
    file_id = get_file_id(conn, file_name)
    with gzip.open(buffer, mode="rt") as fo:
        reader = csv.reader(fo, delimiter="\t")
        _ = next(reader)
        for row in reader:
            if line == 2000:
                break
            body = row[13]
            blob = TextBlob(body)
            if len(body) > 8092:
                body = body[:8092]
            insert_list.append((file_id, row[5], row[7], row[12], body, blob.sentiment[0] * 100))
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
        insert into analysis.review_sentiment
        (reviews_file_id, product_title, star_rating, review_headline, review_body, sentiment)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cur.executemany(insert_stmt, res_list)
    cur.close()


def get_file_id(conn, file_name):
    cur = conn.cursor()
    insert_file = '''
        insert into analysis.reviews_file
        (file_name)
        VALUES (%s)
    '''
    cur.execute(insert_file, (file_name, ))
    select_id = '''
        select reviews_file_id from analysis.reviews_file
        where file_name = %s
    '''
    cur.execute(select_id, (file_name, ))
    id = cur.fetchone()[0]
    cur.close()

    return id
