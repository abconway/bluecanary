class ConfigurationManager(object):

    Configuration = {'plugins': []}

    @classmethod
    def add_plugins_directory(cls, path):
        cls.Configuration['plugins'].append(path)

    @classmethod
    def get_plugins_directories(cls):
        return cls.Configuration.get('plugins')
