import unittest

from bluecanary.tags.elb import get_all_elb_names, process_raw_elb_tags_responses


class TestELBTags(unittest.TestCase):

    def test_get_all_elb_names(self):
        describe_load_balancers_response = {
            'ResponseMetadata': {
                'HTTPStatusCode': 200,
                'RequestId': 'fake-request-id',
            },
            'LoadBalancerDescriptions': [
                {'LoadBalancerName': 'fake-name-1'},
                {'LoadBalancerName': 'fake-name-2'},
                {'LoadBalancerName': 'fake-name-3'},
            ],
        }

        expected_elb_names = [
            'fake-name-1',
            'fake-name-2',
            'fake-name-3',
        ]

        elb_names = get_all_elb_names(describe_load_balancers_response)

        self.assertEqual(expected_elb_names, elb_names)

    def test_process_raw_elb_tags_responses(self):
        describe_tags_responses = [
            {
                'ResponseMetadata': {
                    'HTTPStatusCode': 200,
                    'RequestId': 'fake-request-id',
                },
                'TagDescriptions': [
                    {
                        'LoadBalancerName': 'fake-name-1',
                        'Tags': [
                            {'Key': 'fake-key-1', 'Value': 'fake-value-1'},
                        ],
                    },
                ]
            },
            {
                'ResponseMetadata': {
                    'HTTPStatusCode': 200,
                    'RequestId': 'fake-request-id',
                },
                'TagDescriptions': [
                    {
                        'LoadBalancerName': 'fake-name-2',
                        'Tags': [
                            {'Key': 'fake-key-1', 'Value': 'fake-value-2'},
                        ],
                    },
                ]
            },
            {
                'ResponseMetadata': {
                    'HTTPStatusCode': 200,
                    'RequestId': 'fake-request-id',
                },
                'TagDescriptions': [
                    {
                        'LoadBalancerName': 'fake-name-3',
                        'Tags': [
                            {'Key': 'fake-key-1', 'Value': 'fake-value-3'},
                            {'Key': 'fake-key-2', 'Value': 'fake-value-4'},
                        ],
                    },
                ]
            },
        ]

        expected_result = {
            'fake-name-1': 'fake-key-1:fake-value-1',
            'fake-name-2': 'fake-key-1:fake-value-2',
            'fake-name-3': 'fake-key-1:fake-value-3',
        }

        processed_tags = process_raw_elb_tags_responses(describe_tags_responses,
                                                        'fake-key-1')

        self.assertDictEqual(processed_tags, expected_result)
