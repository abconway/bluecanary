import os
from collections import namedtuple


AWSProfile = namedtuple('AWSProfile', ['AWS_PROFILE',
                                       'AWS_ACCESS_KEY_ID',
                                       'AWS_SECRET_ACCESS_KEY',
                                       'AWS_DEFAULT_REGION'])


class AWSCredentialsManager(object):

    AWS_PROFILES = {}
    SAVED_ENVIRONMENT_STATE = {}

    @classmethod
    def add_aws_profile(cls, aws_profile, aws_access_key_id,
                        aws_secret_access_key, aws_default_region):
        cls.AWS_PROFILES[aws_profile] = AWSProfile(
            AWS_PROFILE=aws_profile,
            AWS_ACCESS_KEY_ID=aws_access_key_id,
            AWS_SECRET_ACCESS_KEY=aws_secret_access_key,
            AWS_DEFAULT_REGION=aws_default_region,
        )

    @classmethod
    def load_aws_profile(cls, aws_profile):
        cls.clean_current_profile()

        profile = cls.AWS_PROFILES.get(aws_profile)

        if profile:
            cls.set_current_profile(profile)
        else:
            os.environ['AWS_PROFILE'] = aws_profile

    @classmethod
    def save_environment_state(cls):
        cls.SAVED_ENVIRONMENT_STATE = {
            'AWS_PROFILE': os.environ.get('AWS_PROFILE'),
            'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'AWS_DEFAULT_REGION': os.environ.get('AWS_DEFAULT_REGION'),
        }

    @classmethod
    def load_saved_environment_state(cls):
        for key, value in cls.SAVED_ENVIRONMENT_STATE.items():
            if value:
                os.environ[key] = value
            else:
                if os.environ.get(key):
                    del(os.environ[key])

    @staticmethod
    def set_current_profile(profile):
        os.environ['AWS_ACCESS_KEY_ID'] = profile.AWS_ACCESS_KEY_ID
        os.environ['AWS_SECRET_ACCESS_KEY'] = profile.AWS_SECRET_ACCESS_KEY
        os.environ['AWS_DEFAULT_REGION'] = profile.AWS_DEFAULT_REGION

    @staticmethod
    def clean_current_profile():
        if os.environ.get('AWS_PROFILE'):
            del(os.environ['AWS_PROFILE'])

        if os.environ.get('AWS_ACCESS_KEY_ID'):
            del(os.environ['AWS_ACCESS_KEY_ID'])

        if os.environ.get('AWS_SECRET_ACCESS_KEY'):
            del(os.environ['AWS_SECRET_ACCESS_KEY'])

        if os.environ.get('AWS_DEFAULT_REGION'):
            del(os.environ['AWS_DEFAULT_REGION'])
