class TagsManager(object):

    TagGroups = {}

    @classmethod
    def add_tag_group(cls, **kwargs):
        key = '{}:{}'.format(kwargs['TagKey'], kwargs['TagValue'])

        cls.TagGroups[key] = kwargs

    @classmethod
    def get_tag_group(cls, tag_key, tag_value):
        key = '{}:{}'.format(tag_key, tag_value)

        return cls.TagGroups.get(key)

    @classmethod
    def get_groups_by_type(cls, group_type):
        return [
            group for group in cls.TagGroups.values()
            if group.get('Type') == group_type
        ]
