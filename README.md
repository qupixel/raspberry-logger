# `raspylog`: Read, Store and Visualize Sensor Measurements with a Raspberry Pi. 

![Image of setup](https://raw.githubusercontent.com/joeserr/raspylog/master/images/humi.jpeg)

This is a setup for the Raspberry Pi that allows: 

1. Reading from a DHT (Digital Humidity-Temperature) Sensor 
2. Logging sensor values locally
3. Visualizing the last readings in a web dashboard from a remote machine

It has been built in a way that allows generalizing easily to any other sensors.

## Setup

### Getting the code ready 

From the RPi, clone this repository, then do 

    cd raspylog
	sudo pip3 install .
	
This will install the `raspylogger` python module in your Pi, so you will be able to execute the scripts in the `scripts` folder.  

### RPi humidity sensor wiring

You need to connect a DHT sensor to the Raspberry Pi's GPIO pins, as explained 
[here](https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/). 

To check that the sensor is working, try: 

    sudo python3 scripts/example_console.py
	
This is a simple example that does not even use the python module and should output a Temperature
and Humidity value to the console. 

## Performing and storing a sensor read

With the RPi connected to the DHT sensor,  now try

    sudo python3 scripts/single_read.py data/sample.h5
	
If the command runs successfully, the temperature and humidity values
have been read and stored to the HDF5 file `data/sample.h5`
(later on a few words on the HDF5 format). 

## Scheduling the readings

The idea is to schedule such a reading, e.g. with `cron`. 

Add a similar line to `/etc/crontab`:

    0-59/20 *  * * *        root    python3 /home/path/to/raspylog/scripts/single_read.py /home/path/to/raspylog/data/yourfile.h5

This will schedule a reading, by calling the command exemplified above, every 20 minutes
(more specifically: at X:00, X:20, and X:40, where X is every hour). Replace the paths
with your paths. 

## Visualizing the readings remotely

You can visualize the readings from another machine in the same network (e.g. another computer,
a tablet or your mobile phone). 

To do so, first run

    python3 scripts/viz.py data/yourfile.h5

This will start a Dash server (a few more words on Dash below). 
The console displays a message like "Running on address 0.0.0.0:8050.
Remember that number (8050), as it's the port number we need next.

Then, from a different machine, open a web browser and type the IP address of the Pi
and the port number. E.g. if the IP address of your pi is 192.168.0.155, then type:

    192.168.0.155:8050
	
After a few seconds you should see something like the screenshot. 

## Working with other sensors

There is a class `SensorLogger` which defines all the logic for reading + logging. 
One just needs to override the `read_sensor()` function to reuse it for any other
case.  

The `read_sensor()` function needs to return a dictionary of sensor readings, and `None`
when a reading fails.

As long as this rule is respected, everything else works. 

Check out the `humidity.py` for the specific example of how the `TemperatureHumiditySensor`
was inheritted from SensorLogger, and proceed analogously. 

## Good python programming practices

While this setup is simple and lightweight, I have tried to follow good python programming practices
from the beginning, even at this scale. This feels good and paves the way for possible future evolutions. 
Here I highlight: 

* Setuptools: Using `setuptools` to package the module according to the standard practice. 
* Developing the library in a way that is agnostic to the sensor, as explained above. This
also allows developing in a machine different from the Pi where you have a proper editor and tools. 
* Test-driven development: The previous point allowed applying test-driven development and
you can see the tests in the (spoiler) `tests` folder. You can run the tests by calling:

     pytest remote develop

(which, BTW, also takes advantage of setuptools). 

* Code style: I tried to follow coding style standards for python and use linters to alert about code style issues.

Note: The tests cover the generic part, and so far we do not have tests for specific sensors,
as they are platform-dependent. 

## On the shoulders of giants

This library builds on great existing open source tools:

* The [Adafruit_DHT](https://github.com/adafruit/Adafruit_Python_DHT) repository, which allows reading from a DHT sensor in one line of code.
* [HDF5](https://support.hdfgroup.org/HDF5/), to store sensor readings. HDF5 and the associated libraries provide a very powerful
way of storing data with good properties such as indexes or compression. Also compatibility
with pandas, which allow simple ways to read and write DataFrames to an HDF5 store.
* [Dash](https://plot.ly/products/dash/), for visualization. Dash is a tool that allows deploying web applications in pure python. 

(And of course, python and the Raspberry Pi!) 

## Known issues

* In the Raspberry Pi Model B, if using git for cloning the repository,
one can experience out of memory problems, due to the limited memory 
of that model (512K). If this is the case, clone using another machine 
in your network and use e.g. scp to transfer the code. 
