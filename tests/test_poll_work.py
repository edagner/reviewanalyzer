import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from review_poller import sqs_receive
from review_worker import s3_read


def test_both():
    work_tuple = sqs_receive()
    s3_read(work_tuple[0])


if __name__ == "__main__":
    test_both()
