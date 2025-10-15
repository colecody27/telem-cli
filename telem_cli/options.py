from enum import Enum

class Unit(Enum):
    # Length / distance
    METERS = "m"
    CENTIMETERS = "cm"
    MILLIMETERS = "mm"
    INCHES = "in"
    FEET = "ft"

    # Temperature
    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    KELVIN = "K"

    # Pressure
    PASCAL = "Pa"
    BAR = "bar"
    PSI = "psi"

    # Acceleration / motion
    METERS_PER_SECOND2 = "m/s^2"
    G_FORCE = "g"
    METERS_PER_SECOND = "m/s"

    # Magnetic / electric
    TESLA = "T"
    VOLT = "V"
    AMPERE = "A"

    # Light / sound
    LUX = "lx"
    DECIBEL = "dB"

    # Gas / concentration
    PARTS_PER_MILLION = "ppm"
    PERCENT = "%"


# Friendly names for CLI users
UNIT_CHOICES = {
    # Length / distance
    "meters": Unit.METERS,
    "centimeters": Unit.CENTIMETERS,
    "millimeters": Unit.MILLIMETERS,
    "inches": Unit.INCHES,
    "feet": Unit.FEET,

    # Temperature
    "celsius": Unit.CELSIUS,
    "fahrenheit": Unit.FAHRENHEIT,
    "kelvin": Unit.KELVIN,

    # Pressure
    "pascal": Unit.PASCAL,
    "bar": Unit.BAR,
    "psi": Unit.PSI,

    # Acceleration / motion
    "meters_per_second2": Unit.METERS_PER_SECOND2,
    "g_force": Unit.G_FORCE,
    "meters_per_second": Unit.METERS_PER_SECOND,

    # Magnetic / electric
    "tesla": Unit.TESLA,
    "volt": Unit.VOLT,
    "ampere": Unit.AMPERE,

    # Light / sound
    "lux": Unit.LUX,
    "decibel": Unit.DECIBEL,

    # Gas / concentration
    "ppm": Unit.PARTS_PER_MILLION,
    "percent": Unit.PERCENT,
}
