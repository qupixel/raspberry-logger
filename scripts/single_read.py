"""Script to perform a single read of a DHT sensor.

Usage: python3 single_read.py filename

Perform a sn¡ingle sensor reading and add the value to the HDF5 store
specified by "filename".

Add this script to your crontab file to schedule the reading periodically.
"""

from raspylogger.humidity import TempHumidityLogger
import sys

slogger = TempHumidityLogger(store_name=sys.argv[1])

slogger.read()
slogger.store()
