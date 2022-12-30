#!/bin/env python
from sys import argv
from time import sleep
import serial

assert argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
ser = serial.Serial(argv[1], 2400, parity=serial.PARITY_NONE, timeout=1)

from comfospot40.create_packet import create_speed_packet

intake = argv[2] == "in"

value = 0
if argv[3][-1] == "h":
    value = int(argv[3][0:-1], 16)
else:
    value = int(argv[3])

print(value)

directiongroup = 0
if len(argv) == 5:
    directiongroup = int(argv[4])

alt = False
if len(argv) == 6:
    print("alt")
    alt = True

packet = create_speed_packet(1, intake, int(value), directiongroup, alt)
print(packet)
print(" ".join([hex(i) for i in packet]))
while True:
    ser.write(packet)
    print("writing")
    # print(com.get_state())
    sleep(1)
