# Zehnder comfospot twin 40

<a href="https://www.buymeacoffee.com/rubenbe" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

To read/write on the bus, use this waveshare adapter. 
[Find it on the waveshare website](https://www.waveshare.com/usb-to-rs232-485-ttl.htm?sku=15817)
Others don't seem to function properly.

Setup:
* Buy the waveshare adapter
* Setup your MQTT server
* In case you want to use home assistant, ensure you run 2023.05 or newer.
* Open the adapter and set the internal jumper to NC.
* Set the voltage to 5V
* Only A+ and B- need to be connected. GND is not connected.
* Disconnect the original touchscreen (switching off is not sufficient). The protocol only supports one master on the bus.
* Connect the adapter via USB and get its name with `ls /dev/tty*` (this might be different depending on system). Usually this will be /dev/ttyUSB0 or similar.
* Clone or download this repo.
* Go to the project folder run `pip install -r requirements.txt`
* Start the server `python server.py --mqtt MQTTIP --dev=/dev/ttySomething --oscillation=60 --sensorvalidity=65 --state=./state.json`
* Run the server as a service or container in order to launch directly after a reboot.Ensure it starts after the MQTT server.

```
python server.py --help
usage: server.py [-h] --mqtt MQTT [--mqtt-port MQTT_PORT] [--mqtt-prefix MQTT_PREFIX] [--dev DEV] [--oscillation OSCILLATION] [--sensorvalidity SENSORVALIDITY] [--state STATE] [--reverse]

options:
  -h, --help            show this help message and exit
  --mqtt MQTT           MQTT address
  --mqtt-port MQTT_PORT
                        MQTT port
  --mqtt-prefix MQTT_PREFIX
                        MQTT prefix
  --dev DEV             Serial device
  --oscillation OSCILLATION
                        Oscillation time in seconds
  --sensorvalidity SENSORVALIDITY
                        Sensor data validity in seconds
  --state STATE         JSON file to store state
  --reverse             Fans are installed reversed
```

# About the comfospot
This seems to be a OEM product by GetAir sold under the Zehnder brand.
It's available under these brand names:
* Zehnder ComfoSpot Twin 40
* Zewotherm Fan
* GetAir SmartFan
* Kermi x-well D12 (in case you don't get a signal, try switching the A and B wires)
* Viessmann Vitovent 100-D


Only the Zehnder has been tested,
but devices from other manufacturers should work as they seem identical.


# Home Assistant
A number of entities will be exposed via MQTT in Home Assistant (2023.05 or newer).
Please not that there is no hard requirement to run home assistant, other MQTT setups should be compatible.

## Fans
For each zone, a fan entity is exposed named `fan.comfospot40_zone_X_fan`. Where `X` ranges from 1 to 3, for each zone.

## Sensors
The sensors are similarly named:
- `fan.comfospot40_zone_X_inside_temperature`
- `fan.comfospot40_zone_X_inside_humidity`
- `fan.comfospot40_zone_1_recycled_temperature`
- `fan.comfospot40_zone_X_recycled_humidity`

## Counter fan setting (advanced)
Also for each zone, a selection entity called `select.comfospot40_zone_X_counter_fan_setting` is exposed.
This is an advanced setting not available on the default controller and allows to modify the settings of the fans with the fourth DIP switch set to 1.
There are four settings:
- **Off**: disable the fans.
- **Always same direction**: always run them in the same direction as the main fan. (effectively disabling the DIP switch behaviour)
- **Always counter direction**: emulate the default behaviour (default).
- **Counter when oscillating**: emulate the default behaviour when the fans are in oscilating mode only.

# Temperature & humidity sensor.
The sensor is a Sensiron SHT21 i2c based sensor.

# Packet specification
## Packet header
* 00 0x55 Preamble
* 01 0x4D Preamble
* 02 0x00 Preamble
* 03 0x96 Preamble
* 04 Data length excluding checksum

## Fan level
The maximum fan level is 100
Setting a fan level of 101 or higher will stop the fan
The minimum fan level seems to be 26 0x1a

## Zones
There are 3 user zones (DIP switch 1 to 3 on the fans).
If none of the DIP 1 to 3 switches is set, the fan joins the first group.

On protocol level there are 6.
In fact the [protocol level] == [user zone - 1] * 2
These are the even zones (DIP switch 4 set to OFF on the fans).

If DIP switch 4 on the fan is set to ON.
The fan will listen to the odd zones.
