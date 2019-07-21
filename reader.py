from sys import argv
import serial
import struct

assert argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
SER = serial.Serial(argv[1], 2400, parity=serial.PARITY_NONE, timeout=1)
def search_length():
    print('y')
    readbytes=SER.read(4)
    #print(readbytes)
    #readints = int.from_bytes(readbytes, "little")
    readints = struct.unpack("<BBBB", readbytes)
    print(readints)
    size = readints[-1]+1
    readbytes=SER.read(size)
    #print(readbytes)
    readints = struct.unpack("<"+"B"*(size), readbytes)
    print(readints)
    return search_preamble

def search_preamble():
    print('x')
    readbyte = SER.read()
    print(readbyte)
    if readbyte == b'\x55':
        return search_length
    return search_preamble

STATE = search_preamble
while True:
    STATE = STATE()

    #readbyte = SER.read()
    #print(readbyte)
    #x = something
    #if readbyte == b'U':
    #    print(SER.read(5))
    #    x()
