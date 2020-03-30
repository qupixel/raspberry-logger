"""Tests for the SensorLogger module."""

import pandas as pd
from raspylogger.sensing import SensorLogger


def test_sense():
    """Test the basic sensor.read_sensor() method."""
    sensor = SensorLogger()
    hum = sensor.read()

    assert(hum is not None)


def test_read():
    """Test sensor.read()."""
    sensor = SensorLogger()
    hum = sensor.read_sensor()

    assert(hum is not None)


def test_store(tmpdir):
    """Test sensor.store()."""
    location = tmpdir.mkdir("sub").join("store.h5")
    sensor = SensorLogger(store_name=location)
    sensor.read()
    sensor.store()

    frm = pd.read_hdf(location, key="readings")

    assert(frm.shape[0] == 1)
    assert(len(frm.columns) == 2)
    assert(frm.iloc[0, :].value == 3.14)
    # Check the first column contains a timestamp
    assert(type(frm.loc[0, 'timestamp']) == pd.Timestamp)


def test_store_multi(tmpdir):
    """Test multiple calls to sensor.store()."""
    N = 10
    location = tmpdir.mkdir("sub").join("store.h5")

    # Perform sensor reading
    sensor = SensorLogger(store_name=location)
    sensor.read()

    # Store N times
    for _ in range(0, N):
        sensor.store()

    # Check file contains N items
    f = pd.read_hdf(location, key="readings")
    assert(f.shape[0] == N)


def test_none(tmpdir):
    """Test a bad reading is handled."""
    location = tmpdir.mkdir("sub").join("store.h5")
    sensor = SensorLogger(store_name=location)
    sensor.read()
    sensor.store()
    sensor.last_reading = None
    sensor.store()

    # Check file contains 1 item
    f = pd.read_hdf(location, key="readings")
    assert(f.shape[0] == 1)
