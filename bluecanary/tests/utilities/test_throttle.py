import unittest

from botocore.exceptions import ClientError

from bluecanary.utilities import throttle


class TestThrottle(unittest.TestCase):
    def test_throttle(self):
        @throttle(max_retries=2, interval=0.001)
        def function():
            error_response = {
                'Error': {
                    'Code': 'TEST',
                    'Message': 'Throttling',
                }
            }
            raise ClientError(error_response=error_response, operation_name='test')

        try:
            function()
        except ClientError as e:
            if 'Throttling' in e.args[0]:
                self.fail('A throttled function should not raise a ClientError '
                          'for throttling.')
            else:
                raise e
