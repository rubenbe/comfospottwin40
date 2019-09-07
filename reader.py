from sys import argv
import logging
import struct
import serial
import comfospot40

assert argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
ser = serial.Serial(argv[1], 2400, parity=serial.PARITY_NONE, timeout=1)
com = comfospot40.Parser(ser)
com.start()
com.join()
