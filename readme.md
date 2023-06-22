Requires home assistant 2023.05 or newer

# Zehnder comfospot twin 40

To read/write on the bus, use a waveshare adapter. 
[Find it on the waveshare website](https://www.waveshare.com/usb-to-rs232-485-ttl.htm?sku=15817)
Others don't seem to function properly

Setup:
* Set the internal jumper to NC.
* Set the voltage to 5V
* Only A+ and B- need to be connected. GND is not connected.
* Disconnect the original touchscreen, as the protocol only supports one master on the bus.

To only read from the bus, a cheap RS485 reader is sufficient.

# About the comfospot
This seems to be a OEM product by GetAir sold under the Zehnder brand.
It's available under these brand names:
* Zehnder ComfoSpot Twin 40
* Zewotherm Fan
* GetAir SmartFan
* Kermi x-well D12


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
