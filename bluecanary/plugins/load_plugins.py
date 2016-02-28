import os
from functools import partial

from pluginbase import PluginBase

from bluecanary.managers import ConfigurationManager


HERE = os.path.abspath((os.path.dirname(__file__)))
get_path = partial(os.path.join, HERE)


plugin_base = PluginBase(
    package='blue_canary_plugins',
    searchpath=[get_path('../builtin_plugins')],
)


class PluginLoader(object):
    def __init__(self):
        self.alarms = {}
        self.source = plugin_base.make_plugin_source(
            searchpath=ConfigurationManager.get_plugins_directories(),
        )
        self.load_plugins()

    def load_plugins(self):
        for plugin_name in self.source.list_plugins():
            plugin = self.source.load_plugin(plugin_name)
            plugin.setup(self)

    def register_alarm(self, name, alarm_class):
        self.alarms[name] = alarm_class


def load_plugins():
    return PluginLoader().alarms
