from functools import wraps
from random import randint
from time import sleep


def exponential_backoff(exception, retries, timeslot):
    """
    When applied to a function, this decorator will attempt to
    retry the function call up to `retries` number of times with
    an exponential backoff between retry attempts.

    After C failures, a random number of timeslots
    between 0 and 2^C - 1 is chosen for the delay.

    See: https://en.wikipedia.org/wiki/Exponential_backoff

    Example::

        @exponential_backoff(ConnectionError, retries=5, timeslot=0.5)
        def network_call(url):
            if randint(0, 4) != 0:
                raise ConnectionError
            return url


        print('Resolved:', network_call('https://google.com'))

    :param exception:   Exception that triggers a retry
    :param retries:     Maximum number of times to retry the function call
    :param timeslot:    Number of seconds a single timeslot occupies
    """
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            retry_attempt = 0
            while retry_attempt < retries:
                try:
                    return func(*args, **kwargs)
                except exception:
                    retry_attempt += 1
                    seconds = randint(0, 2 ** retry_attempt) * timeslot
                    print(f'{exception.__name__}: retrying after {seconds} seconds.')
                    sleep(seconds)
            return func(*args, **kwargs)
        return decorator
    return wrapper
