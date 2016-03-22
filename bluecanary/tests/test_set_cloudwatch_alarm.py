import unittest

from bluecanary.set_cloudwatch_alarm import set_cloudwatch_alarm
from bluecanary.exceptions import NamespaceError


class TestSetCloudwatchAlarm(unittest.TestCase):

    def setUp(self):

        self.identifier = 'i-12345678'
        self.alarm_kwargs = {
            'MetricName': 'CPUUtilization',
            'Statistic': 'Average',
            'Period': 60,
            'EvaluationPeriods': 5,
            'Threshold': 90,
            'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
            'AlarmActions': ['arn:aws:sns:us-east-1:123456789012:test-sns-action'],
            'Namespace': 'AWS/EC2',
        }

    def test_it_fails_if_an_unknown_namespace_is_provided(self):

        alarm_kwargs = self.alarm_kwargs.copy()
        alarm_kwargs['Namespace'] = 'unknown/namespace'

        with self.assertRaises(NamespaceError) as context_manager:
            set_cloudwatch_alarm(identifier=self.identifier, **alarm_kwargs)

        exception = context_manager.exception
        self.assertEqual(
            exception.args[0],
            'Namespace "unknown/namespace" is not supported by Blue Canary. '
            'If you are using a plugin that supports this Namespace please '
            'ensure that the plugin alarm class does not return None when '
            'calling the "get_dimensions" method.'
        )
