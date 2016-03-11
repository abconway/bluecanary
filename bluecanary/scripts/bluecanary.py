#!/usr/bin/env python
import click

from ..utilities.load_yaml import load_path
from .update_alarms import update_ec2_alarms, update_elb_alarms
from .update_tags import update_ec2_tags, update_elb_tags

__version__ = "0.0.5"


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command(help="Tag each resource with the given key/value pair")
@click.option('--path', '-p', type=click.Path(), multiple=True,
              help='File or Directory path to load yaml files from')
@click.option('--verbose', '-v', count=True,
              help='Enable verbose output')
def update_tags(path, verbose):
    load_path(path)

    if verbose:
        click.echo('\nRunning tags update...\n')

    update_ec2_tags(verbose=verbose)
    update_elb_tags(verbose=verbose)


@cli.command(help="Create and/or update alarms for a resource in AWS")
@click.option('--path', '-p', type=click.Path(), multiple=True,
              help='File or Directory path to load yaml files from')
@click.option('--verbose', '-v', count=True,
              help='Enable verbose output')
def update_alarms(path, verbose):
    load_path(path)

    if verbose:
        click.echo('\nRunning alarms update...\n')

    update_ec2_alarms(verbose)
    update_elb_alarms(verbose)
