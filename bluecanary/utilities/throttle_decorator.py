import functools
from time import sleep

from botocore.exceptions import ClientError


DECISECOND = 0.1
MAX_RETRIES = 10


def throttle(max_retries=MAX_RETRIES, interval=DECISECOND):
    def throttle_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            retries = 0
            while retries < max_retries:
                try:
                    sleep((2 ^ retries) * interval)
                    return func(*args, **kwargs)
                except ClientError as e:
                    if 'Throttling' in e.args[0]:
                        retries += 1
                    else:
                        raise e

        return wrapper

    return throttle_decorator
