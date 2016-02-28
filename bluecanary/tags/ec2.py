import click
import boto3

from bluecanary.utilities import throttle


def get_all_ec2_tags(tag_key):
    raw_ec2_tags = get_raw_ec2_tags(tag_key)

    return process_raw_ec2_tags(raw_ec2_tags)


@throttle()
def get_raw_ec2_tags(tag_key):
    ec2_client = boto3.client('ec2')

    return ec2_client.describe_tags(
        Filters=[
            {
                'Name': 'key',
                'Values': [
                    tag_key,
                ]
            },
        ],
    )


def process_raw_ec2_tags(response):
    ec2_tags = dict()

    for ec2 in response.get('Tags'):
        ec2_tags[ec2['ResourceId']] = '{}:{}'.format(ec2['Key'], ec2['Value'])

    return ec2_tags


@throttle()
def set_ec2_tags(instance_ids, tag_key, tag_value, verbose=0):
    if verbose > 1:
        click.echo('Updating the following instances tagged with {}: {}'
                   .format(tag_key, tag_value))
        click.echo(', '.join(instance_ids))
    elif verbose:
        click.echo('Updating instances tagged with {}: {}\n'
                   .format(tag_key, tag_value))

    ec2_client = boto3.client('ec2')

    return ec2_client.create_tags(
        Resources=instance_ids,
        Tags=[
            {
                'Key': tag_key,
                'Value': tag_value,
            },
        ]
    )
