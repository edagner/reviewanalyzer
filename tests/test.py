import time


def test():
    wait_time = 0
    res = 0
    while True:
        if not res:
            time.sleep(wait_time)
            print("waiting {}".format(wait_time))
            wait_time += 5
            print("waiting {} next time".format(wait_time))


if __name__ == "__main__":
    test()
