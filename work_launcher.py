import multiprocessing
import os
import time
from review_worker import Worker


class WorkLauncher(multiprocessing.Process):
    def __init__(self, review_queue):
        super(WorkLauncher, self).__init__()
        self.review_queue = review_queue

    def run(self):
        work_list = list()
        while True:
            if "wrench" in os.listdir():
                print("shutting down")
                break
            elif self.review_queue.qsize() == 0:
                time.sleep(1)
                print("nothing, sleeping")
            elif len(multiprocessing.active_children()) < 4:
                new_work = self.review_queue.get()
                file_name = new_work[0]
                if file_name not in work_list:
                    print("starting work on {}".format(file_name))
                    work_list.append(file_name)
                    reviewer = Worker(new_work)
                    reviewer.start()
                else:
                    pass
