import functools

from bluecanary.managers import AWSCredentialsManager


def preserve_credentials_state(func):
    @functools.wraps(func)
    def manage_credentials_decorator(*args, **kwargs):
        AWSCredentialsManager.save_environment_state()

        func(*args, **kwargs)

        AWSCredentialsManager.load_saved_environment_state()

    return manage_credentials_decorator
