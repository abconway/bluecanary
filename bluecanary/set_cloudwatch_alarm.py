import boto3

from bluecanary.exceptions import NamespaceError
from bluecanary.utilities import throttle


@throttle()
def set_cloudwatch_alarm(identifier, **kwargs):
    if not kwargs.get('Dimensions'):
        kwargs['Dimensions'] = _get_dimensions(identifier, **kwargs)

    if not kwargs.get('AlarmName'):
        kwargs['AlarmName'] = '{}_{}'.format(identifier,
                                             kwargs.get('MetricName'))

    if kwargs.get('AlarmNameModifier'):
        kwargs['AlarmName'] = '{}_{}'.format(kwargs.get('AlarmName'),
                                             kwargs.get('AlarmNameModifier'))
        del(kwargs['AlarmNameModifier'])

    cloudwatch_client = boto3.client('cloudwatch')

    return cloudwatch_client.put_metric_alarm(**kwargs)


def _get_dimensions(identifier, **kwargs):

    base_dimensions = {
        'AWS/ELB': [{u'Name': 'LoadBalancerName', u'Value': identifier}],
        'AWS/EC2': [{u'Name': 'InstanceId', u'Value': identifier}],
    }

    try:
        return base_dimensions[kwargs.get('Namespace')]
    except KeyError:
        message = ('Namespace "{}" is not supported by Blue Canary. '
                   'If you are using a plugin that supports this Namespace '
                   'please ensure that the plugin alarm class does not return '
                   'None when calling the "get_dimensions" method.'
                   .format(kwargs.get('Namespace')))
        raise NamespaceError(message)
