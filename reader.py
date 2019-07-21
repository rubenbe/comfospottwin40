from sys import argv
import struct
import serial

assert argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
SER = serial.Serial(argv[1], 2400, parity=serial.PARITY_NONE, timeout=1)
def search_length():
    print('z')
    readbytes=SER.read(3)
    #print(readbytes)
    #readints = int.from_bytes(readbytes, "little")
    readints = struct.unpack("<BBB", readbytes)
    print(readints)
    size = readints[-1]+1
    readbytes=SER.read(size)
    #print(readbytes)
    readints = struct.unpack("<"+"B"*(size), readbytes)
    print(readints)
    return search_preamble

def search_preamble2():
    print('y')
    readbyte = SER.read()
    readdata = struct.unpack("<B", readbyte)[0]
    print(readdata)
    if readdata == 0x4d:
        return search_length
    if readdata == 0x00:
        return search_length
    if readdata == 0x53:
        return search_length
    if readdata == 0x55:
        return search_preamble2
    return search_preamble

def search_preamble():
    print('x')
    readbyte = SER.read()
    readdata = struct.unpack("<B", readbyte)[0]
    print(readdata)
    if readdata == 0x55:
        return search_preamble2
    return search_preamble

STATE = search_preamble
while True:
    STATE = STATE()
