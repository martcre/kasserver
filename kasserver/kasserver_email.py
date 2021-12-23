from email.policy import default
import logging
from os import name

import click

import kasserver

from pprint import pprint

LOGGER = logging.getLogger(__name__)


@click.group()
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Increase log output verbosity.",
)
@click.version_option(kasserver.__version__)
def cli(verbose):
    """Manage All-Inkl Email Accounts through the KAS server."""
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

@cli.command(name = "list")
@click.argument("login")
def list_command(login):
    """List Emails"""
    kas = kasserver.KasServer()
    records = kas.get_email_records(login)
    
    for item in records:
        pprint(item)


@cli.command(name = "add")
@click.argument("mail")
@click.argument("password")
def add_command(mail, password):
    """Add Email Record"""
    kas = kasserver.KasServer()
    records = kas.add_email_record(mail, password)
    
    for item in records:
        pprint(item)