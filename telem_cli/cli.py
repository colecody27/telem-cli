import click
from telem_cli.api_client import APIClient
from telem_cli.config import get_api_url
import json
from telem_cli.utils import *

@click.group()
@click.option("--api-url", default=get_api_url(), help="Base URL of the backend API.")
@click.pass_context
def cli(ctx, api_url):
    """Sensor CLI — client interface for interacting with the API."""
    ctx.obj = APIClient(api_url)


################ USERS ####################
# LOGIN
@cli.command()
@click.argument("username", type=str)
@click.argument("password", type=str)
@click.pass_obj
def login(client, username, password):
    """Authenticate user and store token."""
    result = client.login(username, password)
    pretty_print_json(result)

# REGISTER
@cli.command()
@click.argument("email", type=str)
@click.argument("username", type=str)
@click.argument("password", type=str)
@click.pass_obj
def register(client, email, username, password):
    """Authenticate user and store token."""
    result = client.register(email, username, password)
    pretty_print_json(result)


################ SENSORS ####################
# REGISTER SENSOR
@cli.command()
@click.argument("type", type=str)
@click.option("--latitude", type=float, help="Latitudinal coordinate in decimal format")
@click.option("--longitude", type=float, help="Longitudinal coordinate in decimal format")
@click.option("--description", type=str, help="Description of sensor")
@click.option("--active/--inactive", default=True, help="Set sensor as active or inactive")
@click.pass_obj
def register_sensor(client, type, latitude, longitude, description, active):
    """Register a new sensor."""
    result = client.register_sensor(type, latitude, longitude, description, active)
    pretty_print_json(result)

# UPDATE SENSOR
@cli.command()
@click.argument("sensor_id", type=int)
@click.option("--type", type=str, help="Type of sensor")
@click.option("--latitude", type=float, help="Latitudinal coordinate in decimal format")
@click.option("--longitude", type=float, help="Longitudinal coordinate in decimal format")
@click.option("--description", type=str, help="Description of sensor")
@click.option("--active/--inactive", default=True, help="Set sensor as active or inactive")
@click.pass_obj
def update_sensor(client, sensor_id, type, latitude, longitude, description, active):
    """Update a sensor."""
    result = client.update_sensor(sensor_id, type, latitude, longitude, description, active)
    pretty_print_json(result)

# GET SENSORS
@cli.command()
@click.pass_obj
def get_sensors(client):
    """Gets metadata for all sensors"""
    result = client.get_sensors()
    pretty_print_json(result)

# GET SENSOR
@cli.command()
@click.argument("sensor_id", type=int)
@click.pass_obj
def get_sensor(client, sensor_id):
    """Gets metadata for all sensors"""
    result = client.get_sensor(sensor_id)
    pretty_print_json(result)

################ DATA ####################
# LOG DATA
@cli.command()
@click.argument("sensor_id", type=int)
@click.argument("unit", type=str)
@click.argument("value", type=float)
@click.pass_obj
def push_sensor_data(client, sensor_id, unit, value):
    """Send a new reading for a sensor."""
    result = client.push_sensor_data(sensor_id, unit, value)
    pretty_print_json(result)

# GET DATA
@cli.command()
@click.argument("sensor_id", type=int)
@click.pass_obj
def get_sensor_data(client, sensor_id):
    """Gets all data for a given sensor"""
    result = client.get_sensor_data(sensor_id)
    pretty_print_json(result)

if __name__ == "__main__":
    cli()
