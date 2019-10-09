import multiprocessing
from work_launcher import WorkLauncher
from review_poller import ReviewPoller


if __name__ == "__main__":
    try:
        manager = multiprocessing.Manager()
        work_queue = manager.Queue()
        rp = ReviewPoller(work_queue)
        rp.start()
        rm = WorkLauncher(work_queue)
        rm.start()

        rp.join()
        rm.join()
    except Exception as e:
        print(e)
