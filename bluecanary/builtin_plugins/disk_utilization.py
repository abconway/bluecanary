import boto3

from bluecanary.plugins.plugin_base_class import PluginBaseClass
from bluecanary.utilities import throttle


class DiskUtilizationAlarm(PluginBaseClass):

    __nonstandard_kwargs__ = ['MountPath']

    @throttle()
    def get_dimensions(self, identifier, **kwargs):
        cloudwatch_client = self.__boto3__.client('cloudwatch')

        response = cloudwatch_client.list_metrics(
            Namespace='System/Linux',
            MetricName='DiskSpaceUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': identifier}]
        )

        lists_of_dimensions = [
            response_group['Dimensions']
            for response_group in response['Metrics']
        ]

        for dimensions in lists_of_dimensions:
            if self._get_mount_path(dimensions) == kwargs.get('MountPath'):
                return dimensions

        # Fail to find any Metrics associated with this instance, return generic Dimensions
        return [
            {'Name': 'Filesystem', 'Value': '/not/found'},
            {'Name': 'InstanceId', 'Value': identifier},
            {'Name': 'MountPath', 'Value': kwargs.get('MountPath')},
        ]

    def get_alarm_name(self, identifier, **kwargs):

        return '{}_DiskSpaceUtilization:{}'.format(
            identifier,
            kwargs.get('MountPath'),
        )

    def _get_mount_path(self, dimensions):

        for dimension in dimensions:
            if dimension['Name'] == 'MountPath':
                return dimension['Value']


def setup(app):
    app.register_alarm(name='DiskSpaceUtilization',
                       alarm_class=DiskUtilizationAlarm())
