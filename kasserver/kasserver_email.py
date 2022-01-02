import logging
from os import name

from tabulate import tabulate

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
@click.option("--login", default=None, help="List only records with login=<Login>")
@click.option("--nofilter", is_flag=True, default=False, help="If True, show all fields")
@click.option("--fields", default="", help="Comma separated list of fields. Will be ignored if -nofilter=True")
def list_command(login, nofilter, fields):
    """List Emails"""
    kas = kasserver.KasServer()
    records = kas.get_email_records(login)

    output = {}
    if nofilter:
        output = records
    else:
        filteredFields = []
        if len(fields) == 0:
            filteredFields = [
                    "mail_login",
                    "mail_adresses",
                    "show_password",
                    "mail_password",
                    "mail_is_active",
                    "in_progress",
                    "mail_copy_adress",
            ]
        else:
            filteredFields = fields.split(',')
        output = [{k:v for (k,v) in record.items() if filteredFields.__contains__(k)} for record in records]
    print(tabulate(output, headers="keys"))

@cli.command(name = "add")
@click.argument("mail")
@click.argument("password")
@click.option("--copyadress", default="")
def add_command(mail, password, copyadress):
    """Add Email Record"""
    kas = kasserver.KasServer()
    mail_login = kas.add_email_record(mail, password, copyadress)
    
    pprint(mail_login)