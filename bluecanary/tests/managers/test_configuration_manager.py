import unittest

from bluecanary.managers import ConfigurationManager


class TestConfigurationManager(unittest.TestCase):
    def setUp(self):
        super(TestConfigurationManager, self).setUp()
        self.configuration = {
            'Plugins': [
                '~/blue-canary/plugins',
                '~/blue-canary/third-party-plugins',
            ]
        }

    def tearDown(self):
        ConfigurationManager.Configuration['plugins'] = []

    def test_add_plugins_directory(self):
        for path in self.configuration.get('Plugins'):
            ConfigurationManager.add_plugins_directory(path)

        self.assertListEqual(ConfigurationManager.Configuration.get('plugins'),
                             self.configuration.get('Plugins'))

    def test_get_plugins_directories(self):
        for path in self.configuration.get('Plugins'):
            ConfigurationManager.add_plugins_directory(path)

        self.assertEqual(len(ConfigurationManager.get_plugins_directories()), 2)
        self.assertEqual(ConfigurationManager.get_plugins_directories(),
                         self.configuration.get('Plugins'))
