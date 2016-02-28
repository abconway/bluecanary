import os
import unittest
from tempfile import NamedTemporaryFile


from bluecanary.managers import (
    AlarmsManager,
    AWSCredentialsManager,
    AWSProfile,
    ConfigurationManager,
    TagsManager,
)
from bluecanary.utilities.load_yaml import load_yaml_file


class TestLoadYaml(unittest.TestCase):
    def setUp(self):
        super(TestLoadYaml, self).setUp()
        fake_data = (
            b'---\n'
            b'Configuration:\n'
            b'  Plugins:\n'
            b'    - ~/plugins\n'
            b'    - ~/other/plugins\n'
            b'AWSProfiles:\n'
            b'  -\n'
            b'    AWS_PROFILE: fake-profile\n'
            b'    AWS_ACCESS_KEY_ID: fake-access-key-id\n'
            b'    AWS_SECRET_ACCESS_KEY: fake-secret-access-key\n'
            b'    AWS_DEFAULT_REGION: fake-region\n'
            b'AlarmGroups:\n'
            b'  -\n'
            b'    AWSProfile: fake-profile\n'
            b'    TagKey: fake-key\n'
            b'    TagValue: fake-value\n'
            b'    Alarms:\n'
            b'      -\n'
            b'        MetricName: fake-metric\n'
            b'        Statistic: Average\n'
            b'        Period: 60\n'
            b'        EvaluationPeriods: 1\n'
            b'        Threshold: 1\n'
            b'        ComparisonOperator: GreaterThanOrEqualToThreshold\n'
            b'        AlarmActions:\n'
            b'          - fake-alarm-action\n'
            b'        Namespace: AWS/EC2\n'
            b'TagGroups:\n'
            b'  -\n'
            b'    AWSProfile: fake-profile\n'
            b'    TagKey: fake-key\n'
            b'    TagValue: fake-value\n'
            b'    Type: EC2\n'
            b'    Resources:\n'
            b'      - fake-resource\n'
        )

        self.tmp_file = NamedTemporaryFile(delete=False)
        self.tmp_file.write(fake_data)
        self.tmp_file.close()

    def tearDown(self):
        super(TestLoadYaml, self).tearDown()
        os.unlink(self.tmp_file.name)
        ConfigurationManager.Configuration['plugins'] = []

    def test_load_yaml_file_loads_aws_profiles_into_the_AWSCredentialsManager(self):
        expected_profile = AWSProfile(
            AWS_PROFILE='fake-profile',
            AWS_ACCESS_KEY_ID='fake-access-key-id',
            AWS_SECRET_ACCESS_KEY='fake-secret-access-key',
            AWS_DEFAULT_REGION='fake-region',
        )

        load_yaml_file(self.tmp_file.name)

        self.assertEqual(AWSCredentialsManager.AWS_PROFILES.get('fake-profile'),
                         expected_profile)

    def test_load_yaml_file_loads_alarm_groups_into_the_AlarmsManager(self):
        expected_group = {
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

        load_yaml_file(self.tmp_file.name)

        self.assertEqual(AlarmsManager.get_alarm_group('fake-key:fake-value'),
                         expected_group)

    def test_load_yaml_file_loads_alarm_groups_into_the_TagsManager(self):
        expected_group = {
            'AWSProfile': 'fake-profile',
            'TagKey': 'fake-key',
            'TagValue': 'fake-value',
            'Type': 'EC2',
            'Resources': ['fake-resource'],
        }

        load_yaml_file(self.tmp_file.name)

        self.assertEqual(TagsManager.get_tag_group('fake-key', 'fake-value'),
                         expected_group)

    def test_load_yaml_file_loads_plugins_into_the_ConfigurationManager(self):
        expected_plugins = ['~/plugins', '~/other/plugins']

        load_yaml_file(self.tmp_file.name)

        self.assertListEqual(ConfigurationManager.get_plugins_directories(),
                             expected_plugins)
