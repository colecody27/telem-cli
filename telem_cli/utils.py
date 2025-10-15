import click
import json

def pretty_print_json(data):
    click.echo(click.style(json.dumps(data, indent=4), fg="green"))
