"""Defines class HumidityLogger to read from a DHT sensor."""

import Adafruit_DHT
from raspylogger.sensing import SensorLogger


DEFAULT_PIN = 22


class TempHumidityLogger(SensorLogger):
    """Class to implement humidity logger."""

    def read_sensor(self, pin=DEFAULT_PIN):
        """Read humidity."""
        sensor = Adafruit_DHT.DHT11
        humedad, temp = Adafruit_DHT.read_retry(sensor, pin)

        if humedad is not None: 
            out = {'humidity': humedad, 'temperature': temp}
        else:
            out = None
        return out
