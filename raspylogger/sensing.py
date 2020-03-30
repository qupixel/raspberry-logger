"""Defines the SensorLogger class."""

import datetime as dt
import logging
import pandas as pd


# Default options
_DEFAULT_KEY = "readings"
_DEFAULT_COMPLEVEL = 6
_DEFAULT_COMPLIB = "bzip2"
_DEFAULT_FORMAT = "table"

# Warning message
WARNING_EMPTY = "Last reading was empty - not storing anything."


class SensorLogger:
    """SensorLogger class."""

    FOO_VALUE = 3.14

    def __init__(self, store_name=None):
        """Initialize class."""
        self.last_reading = None
        self.store_name = store_name

        # Init logger
        self.__logger = logging.getLogger(__name__)

    def read_sensor(self):
        """Read from sensor.

        This is provided for easing test-driven development,
        but should be overriden.

        It must return a dictionary with the sensor reading(s),
        or None of the reading is not successful.
        """
        return {'value': self.FOO_VALUE}

    def read(self):
        """Read and store last reading internally."""
        self.last_reading = self.read_sensor()
        return self.last_reading

    def store(self):
        """Store last reading."""
        if self.last_reading is not None:
            today = dt.datetime.today()
            aux_frame = pd.DataFrame(self.last_reading, index=[0])
            aux_frame['timestamp'] = today

            pd.DataFrame(aux_frame).to_hdf(
                    path_or_buf=self.store_name,
                    key=_DEFAULT_KEY,
                    data_columns=[],
                    format=_DEFAULT_FORMAT,
                    complevel=_DEFAULT_COMPLEVEL,
                    complib=_DEFAULT_COMPLIB,
                    append=True,
                )
        else:
            self.__logger.warning(WARNING_EMPTY)
