import unittest

from bluecanary.tags.ec2 import process_raw_ec2_tags


class TestEC2Tags(unittest.TestCase):
    def test_process_raw_ec2_tags_data_extracts_the_instance_id_and_tag_value(self):
        ec2_tags_describe_response = {
            'ResponseMetadata': {
                'HTTPStatusCode': 200,
                'RequestId': 'fake-request-id',
            },
            'Tags': [
                {
                    'Key': 'fake_key_1',
                    'Value': 'fake_value_1',
                    'ResourceId': 'i-fakeres1',
                    'ResourceType': 'instance',
                },
                {
                    'Key': 'fake_key_1',
                    'Value': 'fake_value_2',
                    'ResourceId': 'i-fakeres2',
                    'ResourceType': 'instance',
                },
                {
                    'Key': 'fake_key_1',
                    'Value': 'fake_value_3',
                    'ResourceId': 'i-fakeres3',
                    'ResourceType': 'instance',
                },
            ]
        }

        expected_result = {
            'i-fakeres1': 'fake_key_1:fake_value_1',
            'i-fakeres2': 'fake_key_1:fake_value_2',
            'i-fakeres3': 'fake_key_1:fake_value_3',
        }

        processed_tags = process_raw_ec2_tags(ec2_tags_describe_response)

        self.assertDictEqual(processed_tags, expected_result)

    def test_process_raw_ec2_tags_returns_empty_dict_if_tags_not_found(self):
        ec2_tags_describe_response = {
            'ResponseMetadata': {
                'HTTPStatusCode': 200,
                'RequestId': 'fake-request-id',
            },
            'Tags': []
        }

        expected_result = dict()

        processed_tags = process_raw_ec2_tags(ec2_tags_describe_response)

        self.assertDictEqual(processed_tags, expected_result)
