# Zehnder comfospot twin 40

Reads out data from the RS485 line in a comfospot twin 40 setup.
A cheap RS485 reader is sufficient.
Only tested with python 3

# About the comfospot
This seems to be a OEM product rebranded by/for Zehnder.
It's available too under these brand names:
* Zewotherm Fan
* GetAir SmartFan

These devices has not been tested, but should work as they seem identical.

# Active control
Currently the software only eavesdrops on the communication
between the controller and the fans.
The goal is to have active control too, but unfortunately the protocol
only supports one master (the controller).
It's not trivial to have your PC override the fan levels of the controller,
because the latter continuously repeats its requests.
As proof of concept, I've been able to control the fans
using a replayed signal from the oscilloscope.
I want to keep the controller installed for easy touch screen control.
