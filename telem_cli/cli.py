import click
from telem_cli.api_client import APIClient
from telem_cli.config import get_api_url
import json
from telem_cli.utils import *
from requests import post
from telem_cli.sensor_reader import *
from telem_cli.options import *
import os 
import pandas as pd

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

# DELETE SENSOR
@cli.command()
@click.argument("sensor_id", type=int)
@click.pass_obj
def remove_sensor(client, sensor_id):
    """Delete sensor and associated data"""
    result = client.delete_sensor(sensor_id)
    pretty_print_json(result)

################ DATA ####################
# LOG SINGLE DATA POINT
@cli.command()
@click.argument("sensor_id", type=int)
@click.argument("unit", type=str)
@click.argument("value", type=float)
@click.option("--file", type=str, help="Name of json or csv file")
@click.pass_obj
def log_sensor_data(client, sensor_id, unit, value):
    """Send a new reading for a sensor."""
    req = {'readings': [{'sensor_id': sensor_id, 'unit': unit, 'value': value}]}
    result = client.push_sensor_data(req)
    pretty_print_json(result)

# LOG DATA POINTS FROM FILE 
@cli.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--batch-size", default=50, show_default=True, help="Number of data points to send per request")
@click.pass_obj
def log_file_data(client, filename, batch_size):
    try:
        # Determine file type
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".csv":
            df = pd.read_csv(filename)
        elif ext == ".json":
            df = pd.read_json(filename)
        else:
            click.echo("Unsupported file type. Please use .csv or .json.")
            return

        # Validate required columns
        required_cols = {"sensor_id", "unit", "value"}
        if not required_cols.issubset(df.columns):
            click.echo(f"Missing required columns. Found: {list(df.columns)}")
            return
        else:
            df = df[list(required_cols)]

        # Process in batches
        total = len(df)
        click.echo(f"Loaded {total} data points from {filename}")
        for start in range(0, total, batch_size):
            batch = df.iloc[start:start + batch_size].to_dict(orient="records")
            req = {'readings': batch}
            result = client.push_sensor_data(req)
            click.echo(f"Sent batch {start // batch_size + 1} → {len(batch)} records")
            pretty_print_json(result)
        
        click.echo("All data sent successfully!")

    except Exception as e:
        click.echo(f"Error reading or sending data: {e}")

# LOG STREAM OF DATA
@cli.command()
@click.option("--sensor-id", required=True, type=int)
@click.option("--port", default='/dev/cu.usbmodem1101', help="Serial port of Arduino, e.g., /dev/ttyACM0")
@click.option("--baud", default=9600)
@click.option("--batch-size", default=10)
@click.option("--unit", required=True, type=click.Choice(list(UNIT_CHOICES.keys())))
@click.pass_obj
def log_stream_data(client, sensor_id, port, baud, batch_size, unit):
    req = {'readings': []}
    click.echo(f"Attempting to read live data from {port} (baud {baud})")

    for reading in read_from_arduino(port, unit, baud):
        req["readings"].append(reading)
        click.echo(f"Reading gathered: {reading}")

        if len(req["readings"]) >= batch_size:
            print(f'Batch size reached')
            retries = 1
            resp = client.push_sensor_data(sensor_id, req)
            while 'error' in resp and retries < 3:
                click.echo('Error pushing data, retrying...')
                resp = client.push_sensor_data(sensor_id, unit, req)
            
            pretty_print_json(resp)
            req["readings"] = []

# GET DATA
@cli.command()
@click.argument("sensor_id", type=int)
@click.option("--days", type=int)
@click.option("--hours", type=int)
@click.option("--mins", type=int)
@click.pass_obj
def get_sensor_data(client, sensor_id, days, hours, mins):
    """Gets all data for a given sensor"""
    filters = {'filters': {
        'days': days,
        'hours': hours,
        'mins': mins}}

    result = client.get_sensor_data(sensor_id, filters)
    pretty_print_json(result)

# DELETE DATA
@cli.command()
@click.argument("sensor_id", type=int)
@click.option("--data_id", type=int)
@click.pass_obj
def remove_sensor_data(client, sensor_id, data_id):
    """Delete data point for a given sensor"""
    result = client.delete_sensor_data(sensor_id, data_id)
    pretty_print_json(result)

if __name__ == "__main__":
    cli()
