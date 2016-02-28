from bluecanary.plugins import PluginBaseClass


class MemoryUtilizationAlarm(PluginBaseClass):
    def get_dimensions(self, identifier, **kwargs):
        return [{'Name': 'InstanceId', 'Value': identifier}]

    def get_alarm_name(self, identifier, **kwargs):
        return '{}_MemoryUtilization'.format(identifier)


def setup(app):
    app.register_alarm(name='MemoryUtilization', alarm_class=MemoryUtilizationAlarm())
