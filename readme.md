Supports home assistant 2023.05 or newer

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
* Disconnect the original touchscreen, as the protocol only supports one master on the bus.
* After cloning this repo, run `pip install -r requirements.txt`
* Start the server `python server.py --mqtt MQTTIP --dev=/dev/ttySomething --oscillation=60 --sensorvalidity=65 --state=./state.json`

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
