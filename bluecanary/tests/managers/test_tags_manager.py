import unittest

from bluecanary.managers import TagsManager


class TestTagsManager(unittest.TestCase):
    def setUp(self):
        super(TestTagsManager, self).setUp()

        self.tag_group = {
            'AWSProfile': 'fake-profile',
            'TagKey': 'fake-key',
            'TagValue': 'fake-value',
            'Type': 'EC2',
            'Resources': ['fake-resource'],
        }

    def test_add_tag_group(self):
        TagsManager.add_tag_group(**self.tag_group)

        self.assertEqual(TagsManager.TagGroups.get('fake-key:fake-value'),
                         self.tag_group)

    def test_get_tag_group(self):
        TagsManager.add_tag_group(**self.tag_group)

        self.assertEqual(TagsManager.get_tag_group('fake-key', 'fake-value'),
                         self.tag_group)

    def test_get_groups_by_type(self):
        TagsManager.add_tag_group(**self.tag_group)

        self.assertEqual([self.tag_group], TagsManager.get_groups_by_type('EC2'))
