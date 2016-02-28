import abc

import boto3


class PluginBaseClass(object):

    __boto3__ = boto3
    __metaclass__ = abc.ABCMeta
    __nonstandard_kwargs__ = None

    def get_updated_alarm_kwargs(self, identifier, **kwargs):
        if not kwargs.get('Dimensions'):
            kwargs['Dimensions'] = self.get_dimensions(identifier, **kwargs)

        if not kwargs.get('AlarmName'):
            kwargs['AlarmName'] = self.get_alarm_name(identifier, **kwargs)

        if self.__nonstandard_kwargs__:
            for kwarg in self.__nonstandard_kwargs__:
                kwargs.pop(kwarg, None)

        return kwargs

    @abc.abstractmethod
    def get_dimensions(self, identifier, **kwargs):
        """Return the AWS dimensions required to create this type of alarm."""
        return

    @abc.abstractmethod
    def get_alarm_name(self, identifier, **kwargs):
        """Return a string of the name you'd like this type of alarm to have."""
        return
