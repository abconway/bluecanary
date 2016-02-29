import os
from os.path import isfile, isdir

import click
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from bluecanary.managers import (
    AlarmsManager,
    AWSCredentialsManager,
    ConfigurationManager,
    TagsManager,
)


def load_path(path):
    if not path:
        click.echo('Please provide either a file or directory path')
        exit(1)
    else:
        paths = path

    for path in paths:
        if isfile(path):
            load_yaml_file(path)
        elif isdir(path):
            load_yaml_directory(path)


def load_yaml_file(filepath):
    with open(filepath) as fp:
        parse_data(load(fp, Loader=Loader))


def load_yaml_directory(path=None):

    if not path:
        path = os.path.dirname(os.path.realpath(__file__))

    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith('.yaml') or filename.lower().endswith('.yml'):
                load_yaml_file(os.path.join(dirpath, filename))


def parse_data(data):
    for profile in data.get('AWSProfiles', []):
        AWSCredentialsManager.add_aws_profile(
            aws_profile=profile['AWS_PROFILE'],
            aws_access_key_id=profile['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=profile['AWS_SECRET_ACCESS_KEY'],
            aws_default_region=profile['AWS_DEFAULT_REGION'],
        )

    for alarm_group in data.get('AlarmGroups', []):
        AlarmsManager.add_alarm_group(**alarm_group)

    for tag_group in data.get('TagGroups', []):
        TagsManager.add_tag_group(**tag_group)

    if data.get('Configuration'):
        for directory_path in data.get('Configuration').get('Plugins', []):
            ConfigurationManager.add_plugins_directory(directory_path)
