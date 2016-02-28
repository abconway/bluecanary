import unittest

from bluecanary.plugins import load_plugins, PluginBaseClass


class TestLoadPlugins(unittest.TestCase):
    def test_load_plugins(self):
        plugins = load_plugins()

        self.assertIn('DiskSpaceUtilization', plugins.keys())
        self.assertTrue(isinstance(plugins['DiskSpaceUtilization'], PluginBaseClass))

        self.assertIn('MemoryUtilization', plugins.keys())
        self.assertTrue(isinstance(plugins['MemoryUtilization'], PluginBaseClass))
