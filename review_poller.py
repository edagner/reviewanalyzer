import boto3
import time
import os
import multiprocessing
from config import QUEUE_URL
from ast import literal_eval
try:
    from aws_config import ACCESS_ID, ACCESS_KEY
except ImportError:
    ACCESS_ID, ACCESS_KEY = None, None


sqs = boto3.client(
    'sqs',
    aws_access_key_id=ACCESS_ID,
    aws_secret_access_key=ACCESS_KEY,
    region_name='us-east-2')


class ReviewPoller(multiprocessing.Process):
    def __init__(self, review_queue):
        super(ReviewPoller, self).__init__()
        self.review_queue = review_queue

    def run(self):
        wait_time = 0
        while True:
            if "wrench" in os.listdir():
                break
            msg = sqs_receive()
            if not msg:
                time.sleep(wait_time)
                print("waiting {}".format(wait_time))
                wait_time += 5
                print("waiting {} next time".format(wait_time))
                if wait_time == 600:
                    wait_time = 0
            else:
                self.review_queue.put(msg)
                wait_time = 0


def sqs_receive():
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=20,
        WaitTimeSeconds=5
    )
    try:
        message = response['Messages'][0]
    except KeyError:
        return None
    message_body = literal_eval(message["Body"])
    file_object = message_body["Records"][0]["s3"]["object"]["key"]
    receipt_handle = message['ReceiptHandle']

    return (file_object, receipt_handle)

if __name__ == "__main__":
    sqs_receive()
