class AlarmsManager(object):

    AlarmGroups = {}

    @classmethod
    def add_alarm_group(cls, **kwargs):
        key = '{}:{}'.format(kwargs['TagKey'], kwargs['TagValue'])

        cls.AlarmGroups[key] = kwargs

    @classmethod
    def get_alarm_group(cls, key):
        return cls.AlarmGroups.get(key)

    @classmethod
    def get_alarm_keys(cls):
        return cls.AlarmGroups.keys()
