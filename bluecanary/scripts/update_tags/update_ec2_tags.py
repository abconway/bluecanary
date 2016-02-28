import click

from bluecanary.tags import set_ec2_tags
from bluecanary.managers import AWSCredentialsManager, TagsManager
from bluecanary.utilities import preserve_credentials_state


@preserve_credentials_state
def update_ec2_tags(verbose=0):
    if verbose:
        click.echo('Updating EC2 tags\n')

    for group in TagsManager.get_groups_by_type('EC2'):
        AWSCredentialsManager.load_saved_environment_state()
        if group.get('AWSProfile'):
            AWSCredentialsManager.load_aws_profile(group['AWSProfile'])

        set_ec2_tags(instance_ids=group.get('Resources'),
                     tag_key=group.get('TagKey'),
                     tag_value=group.get('TagValue'),
                     verbose=verbose)
