"""Simple humidity & temperature reading example."""

import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 22

humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)

print("Humedad", humedad)
print("Temperatura", temperatura)
