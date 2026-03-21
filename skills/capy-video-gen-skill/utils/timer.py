import time
from functools import wraps


class Timer:
    def __init__(
        self,
        prefix: str = "Start at {start_time}",
        postfix: str = "End at {end_time}, took {duration} seconds.",
    ):
        self.prefix = prefix
        self.format = format
        self.postfix = postfix

    def __call__(
        self,
        func,
    ):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            prefix = self.prefix.replace("{start_time}", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
            print(prefix)

            result = await func(*args, **kwargs)

            end_time = time.time()
            duration = end_time - start_time
            postfix = self.postfix.replace("{end_time}", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))).replace("{duration}", f"{duration:.2f}")
            print(postfix)

            return result

        return wrapper


    def __enter__(self):
        self.start_time = time.time()
        prefix = self.prefix.replace("{start_time}", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time)))
        print(prefix)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False

        end_time = time.time()
        duration = end_time - self.start_time
        postfix = self.postfix.replace("{end_time}", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))).replace("{duration}", f"{duration:.2f}")
        print(postfix)
        return False





if __name__ == "__main__":
    with Timer(
        prefix="Begin timing at {start_time}",
        postfix="Finished at {end_time}",
    ):
        time.sleep(1)


    @Timer()
    def test_sleep():
        time.sleep(1)

    test_sleep()