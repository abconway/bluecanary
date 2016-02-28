import os
import unittest

from bluecanary.managers import AWSProfile, AWSCredentialsManager


class TestAWSCredentialsManager(unittest.TestCase):
    def test_save_environment_state(self):
        os.environ['AWS_PROFILE'] = 'test_profile'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_id'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_secret'
        os.environ['AWS_DEFAULT_REGION'] = 'test_region'

        AWSCredentialsManager.save_environment_state()

        self.assertDictEqual(AWSCredentialsManager.SAVED_ENVIRONMENT_STATE,
                             {
                                 'AWS_PROFILE': 'test_profile',
                                 'AWS_ACCESS_KEY_ID': 'test_id',
                                 'AWS_SECRET_ACCESS_KEY': 'test_secret',
                                 'AWS_DEFAULT_REGION': 'test_region',
                             })

    def test_clean_current_profile(self):
        os.environ['AWS_PROFILE'] = 'test_profile'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_id'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_secret'
        os.environ['AWS_DEFAULT_REGION'] = 'test_region'

        AWSCredentialsManager.clean_current_profile()

        self.assertEqual(os.environ.get('AWS_PROFILE'), None)
        self.assertEqual(os.environ.get('AWS_ACCESS_KEY_ID'), None)
        self.assertEqual(os.environ.get('AWS_SECRET_ACCESS_KEY'), None)
        self.assertEqual(os.environ.get('AWS_DEFAULT_REGION'), None)

    def test_load_saved_environment_state(self):
        os.environ['AWS_PROFILE'] = 'test_profile'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test_id'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test_secret'
        os.environ['AWS_DEFAULT_REGION'] = 'test_region'

        AWSCredentialsManager.save_environment_state()
        AWSCredentialsManager.clean_current_profile()
        AWSCredentialsManager.load_saved_environment_state()

        self.assertEqual(os.environ.get('AWS_PROFILE'), 'test_profile')
        self.assertEqual(os.environ.get('AWS_ACCESS_KEY_ID'), 'test_id')
        self.assertEqual(os.environ.get('AWS_SECRET_ACCESS_KEY'), 'test_secret')
        self.assertEqual(os.environ.get('AWS_DEFAULT_REGION'), 'test_region')

    def test_set_current_profile(self):
        AWSCredentialsManager.clean_current_profile()

        profile = AWSProfile(
            AWS_PROFILE='test_profile',
            AWS_ACCESS_KEY_ID='test_id',
            AWS_SECRET_ACCESS_KEY='test_secret',
            AWS_DEFAULT_REGION='test_region',
        )

        AWSCredentialsManager.set_current_profile(profile)

        self.assertEqual(os.environ.get('AWS_PROFILE'), None)
        self.assertEqual(os.environ.get('AWS_ACCESS_KEY_ID'), 'test_id')
        self.assertEqual(os.environ.get('AWS_SECRET_ACCESS_KEY'), 'test_secret')
        self.assertEqual(os.environ.get('AWS_DEFAULT_REGION'), 'test_region')

    def test_add_aws_profile(self):
        AWSCredentialsManager.clean_current_profile()

        expected_profile = AWSProfile(
            AWS_PROFILE='test_profile',
            AWS_ACCESS_KEY_ID='test_id',
            AWS_SECRET_ACCESS_KEY='test_secret',
            AWS_DEFAULT_REGION='test_region',
        )

        AWSCredentialsManager.add_aws_profile(
            aws_profile='test_profile',
            aws_access_key_id='test_id',
            aws_secret_access_key='test_secret',
            aws_default_region='test_region',
        )

        self.assertEqual(AWSCredentialsManager.AWS_PROFILES.get('test_profile'),
                         expected_profile)

    def test_load_aws_profile(self):
        AWSCredentialsManager.clean_current_profile()

        AWSCredentialsManager.add_aws_profile(
            aws_profile='test_profile',
            aws_access_key_id='test_id',
            aws_secret_access_key='test_secret',
            aws_default_region='test_region',
        )

        AWSCredentialsManager.load_aws_profile('test_profile')

        self.assertEqual(os.environ.get('AWS_PROFILE'), None)
        self.assertEqual(os.environ.get('AWS_ACCESS_KEY_ID'), 'test_id')
        self.assertEqual(os.environ.get('AWS_SECRET_ACCESS_KEY'), 'test_secret')
        self.assertEqual(os.environ.get('AWS_DEFAULT_REGION'), 'test_region')

        AWSCredentialsManager.load_aws_profile('test_another_profile')

        self.assertEqual(os.environ.get('AWS_PROFILE'), 'test_another_profile')
        self.assertEqual(os.environ.get('AWS_ACCESS_KEY_ID'), None)
        self.assertEqual(os.environ.get('AWS_SECRET_ACCESS_KEY'), None)
        self.assertEqual(os.environ.get('AWS_DEFAULT_REGION'), None)
