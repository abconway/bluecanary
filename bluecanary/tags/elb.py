import click
import boto3

from bluecanary.utilities import throttle


MAX = 20


def get_all_elb_tags(tag_key):
    response = get_raw_elbs()
    all_elb_names = get_all_elb_names(response)
    raw_elb_tags_responses = get_raw_elb_tags_responses(all_elb_names)

    return process_raw_elb_tags_responses(raw_elb_tags_responses, tag_key)


@throttle()
def get_raw_elbs():
    elb_client = boto3.client('elb')

    return elb_client.describe_load_balancers()


def get_all_elb_names(response):
    return [elb.get('LoadBalancerName') for elb in response['LoadBalancerDescriptions']]


@throttle()
def get_raw_elb_tags_responses(elb_names):
    def _elb_names_generator(elb_names):
        for index in range(0, len(elb_names), MAX):
            yield elb_names[index:index + MAX]

    elb_client = boto3.client('elb')

    responses = []

    for group_of_elb_names in _elb_names_generator(elb_names):
        responses.append(elb_client.describe_tags(LoadBalancerNames=group_of_elb_names))

    return responses


def process_raw_elb_tags_responses(responses, tag_key):
    def _convert_raw_list_to_dict(elb_tags_list):
        return {
            elb.get('LoadBalancerName'): _get_key_value_pair(elb.get('Tags'), tag_key)
            for elb in elb_tags_list
        }

    def _get_key_value_pair(tags_list, tag_key):
        for tag in tags_list:
            if tag.get('Key') == tag_key:
                return '{}:{}'.format(tag.get('Key'), tag.get('Value'))
        else:
            return None

    all_raw_elb_tags = []

    for response in responses:
        all_raw_elb_tags += response.get('TagDescriptions')

    return _convert_raw_list_to_dict(all_raw_elb_tags)


def set_elb_tags(elb_names, tag_key, tag_value, verbose=0):
    @throttle()
    def _set_elb_tags(elb_name, tag_key, tag_value, verbose=0):
        if verbose > 2:
            click.echo('Updating {}'.format(elb_name))

        elb_client = boto3.client('elb')

        elb_client.add_tags(
            LoadBalancerNames=[elb_name],
            Tags=[
                {
                    'Key': tag_key,
                    'Value': tag_value,
                },
            ]
        )

    if verbose > 1:
        click.echo('Updating the following load balancers tagged with {}: {}'
                   .format(tag_key, tag_value))
        click.echo(', '.join(elb_names))
    elif verbose:
        click.echo('Updating load balancers tagged with {}: {}\n'
                   .format(tag_key, tag_value))

    for elb_name in elb_names:
        _set_elb_tags(elb_name, tag_key, tag_value, verbose)
