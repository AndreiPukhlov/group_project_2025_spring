import time


def time_count(func):
    def time_wrapper():
        start = time.time()
        func()
        end = time.time()
        result = end - start
        if result < 60:
            if result < 2:
                print(f"It takes {round(result)} second")
            else:
                print(f"It takes {round(result)} seconds")

        else:
            if result < 120:
                print(f"It takes {round(result / 60)} minute and {round(result % 60)} seconds")
            else:
                print(f"It takes {round(result / 60)} minutes and {round(result % 60)} seconds")

    return time_wrapper
