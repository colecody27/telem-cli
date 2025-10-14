import click
from telem_cli.api_client import APIClient
from telem_cli.config import get_api_url

@click.group()
@click.option("--api-url", default=get_api_url(), help="Base URL of the backend API.")
@click.pass_context
def cli(ctx, api_url):
    """Sensor CLI — client interface for interacting with the API."""
    ctx.obj = APIClient(api_url)

@cli.command()
@click.argument("username")
@click.argument("password")
@click.pass_obj
def login(client, username, password):
    """Authenticate user and store token."""
    result = client.login(username, password)
    click.echo("✅ Logged in successfully." if result["status"] == "success" else "❌ Login failed.")

@cli.command()
@click.argument("type")
@click.argument("latitude")
@click.argument("longitude")
@click.argument("description")
@click.pass_obj
def register_sensor(client, type, latitude, longitude, description):
    """Register a new sensor."""
    sensor = client.register_sensor(type, latitude, longitude, description)
    click.echo(f"✅ Sensor created: {sensor}")

@cli.command()
@click.argument("sensor_id", type=int)
@click.argument("unit", type=str)
@click.argument("value", type=float)
@click.pass_obj
def push_sensor_data(client, sensor_id, unit, value):
    """Send a new reading for a sensor."""
    data = client.push_sensor_data(sensor_id, unit, value)
    click.echo(f"📡 Data point created: {data}")

@cli.command()
@click.argument("sensor_id", type=int)
@click.pass_obj
def get_sensor_data(client, sensor_id):
    """Gets all data for a given sensor"""
    data = client.get_sensor_data(sensor_id)
    click.echo(data)

if __name__ == "__main__":
    cli()
