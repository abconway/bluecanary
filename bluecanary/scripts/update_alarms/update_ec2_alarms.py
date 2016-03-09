import click

from bluecanary.managers import AlarmsManager, AWSCredentialsManager
from bluecanary.plugins import load_plugins
from bluecanary.set_cloudwatch_alarm import set_cloudwatch_alarm
from bluecanary.tags import get_all_ec2_tags
from bluecanary.utilities import preserve_credentials_state


@preserve_credentials_state
def update_ec2_alarms(verbose=0):
    plugin_alarms = load_plugins()
    alarm_keys = AlarmsManager.get_alarm_keys()

    for alarm_key in alarm_keys:
        alarm_group = AlarmsManager.get_alarm_group(alarm_key)

        tag_key = alarm_group.get('TagKey')
        tag_value = alarm_group.get('TagValue')

        AWSCredentialsManager.load_saved_environment_state()
        if alarm_group.get('AWSProfile'):
            AWSCredentialsManager.load_aws_profile(alarm_group['AWSProfile'])

        ec2_tags = get_all_ec2_tags(tag_key)

        for instance_id, key in ec2_tags.items():
            if key != alarm_key:
                continue

            if verbose:
                click.echo('\nUpdating instance {} tagged with {}: {}'
                           .format(instance_id, tag_key, tag_value))

            alarms = alarm_group.get('Alarms', [])
            for alarm in alarms:
                if verbose:
                    click.echo('Updating {} alarm on instance {}'
                               .format(alarm['MetricName'], instance_id))

                if alarm['MetricName'] in plugin_alarms:
                    alarm = plugin_alarms.get(alarm['MetricName']).get_updated_alarm_kwargs(
                        identifier=instance_id,
                        **alarm
                    )

                set_cloudwatch_alarm(instance_id, **alarm)
