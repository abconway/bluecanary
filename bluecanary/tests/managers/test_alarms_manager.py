import unittest

from bluecanary.managers import AlarmsManager


class TestAlarmsManager(unittest.TestCase):
    def setUp(self):
        super(TestAlarmsManager, self).setUp()
        self.alarm_group = {
            'AWSProfile': 'fake-profile',
            'TagKey': 'fake-key',
            'TagValue': 'fake-value',
            'Alarms': [
                {
                    'MetricName': 'fake-metric',
                    'Statistic': 'Average',
                    'Period': 60,
                    'EvaluationPeriods': 1,
                    'Threshold': 1,
                    'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
                    'AlarmActions': [
                        'fake-alarm-action',
                    ],
                    'Namespace': 'AWS/EC2',
                },
            ],
        }

    def test_add_alarm_group(self):
        AlarmsManager.add_alarm_group(**self.alarm_group)

        self.assertEqual(AlarmsManager.AlarmGroups.get('fake-key:fake-value'),
                         self.alarm_group)

    def test_get_alarm_group(self):
        AlarmsManager.add_alarm_group(**self.alarm_group)

        self.assertEqual(AlarmsManager.get_alarm_group('fake-key:fake-value'),
                         self.alarm_group)

    def test_get_alarm_keys(self):
        AlarmsManager.add_alarm_group(**self.alarm_group)

        self.assertEqual(list(AlarmsManager.get_alarm_keys()),
                         ['fake-key:fake-value'])
