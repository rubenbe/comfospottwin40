#!/bin/env python
from sys import argv
from time import sleep
import serial

assert argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
ser = serial.Serial(argv[1], 2400, parity=serial.PARITY_NONE, timeout=1)

from comfospot40.create_packet import create_speed_packet

zone = int(argv[2])

intake = argv[3] == "in"

value = 0
if argv[4][-1] == "h":
    value = int(argv[4][0:-1], 16)
else:
    value = int(argv[4])

print(value)

directiongroup = 0
if len(argv) == 6:
    directiongroup = int(argv[5])

alt = False
if len(argv) == 7:
    print("alt")
    alt = True

packet = create_speed_packet(zone, intake, int(value), directiongroup, alt)
print(packet)
print(" ".join([hex(i) for i in packet]))
while True:
    ser.write(packet)
    print("writing")
    # print(com.get_state())
    sleep(1)
