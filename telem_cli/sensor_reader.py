# sensor_reader.py
import click
import serial
from datetime import datetime
import time
import math
from telem_cli.options import UNIT_CHOICES

def read_from_arduino(port="/dev/cu.usbmodem1101", unit="meters", baud=9600, timeout=1):
    """Open serial port and yield readings line by line."""
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    time.sleep(2) 
    click.echo(f'Port is open!') if ser.is_open else click.echo(f"Serial port {port} isn't open. Verify the correct port been provided") 
        
    while True:
        line = ser.readline().decode("utf-8").strip()
        if not line:
            continue
        try:
            dist = float(line)
            if math.isnan(dist):
                continue
            yield {
                "unit": UNIT_CHOICES[unit].value,
                "value": dist
            }
        except ValueError:
            # Skip malformed line
            continue
