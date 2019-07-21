from sys import argv
import logging
import struct
import serial

assert argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
SER = serial.Serial(argv[1], 2400, parity=serial.PARITY_NONE, timeout=1)
def search_length(data):
    logging.info('z')
    readbytes=SER.read(3)
    #print(readbytes)
    #readints = int.from_bytes(readbytes, "little")
    readints = struct.unpack("<BBB", readbytes)
    data.extend(readints)
    logging.info(readints)
    size = readints[-1]+1
    readbytes=SER.read(size)
    #print(readbytes)
    readints = struct.unpack("<"+"B"*(size), readbytes)
    data.extend(readints)
    logging.info(readints)
    print(data)
    return data, search_preamble

def search_preamble2(data):
    logging.info('y')
    readbyte = SER.read()
    readdata = struct.unpack("<B", readbyte)[0]
    logging.info(readdata)
    if readdata in (0x4d, 0x00, 0x53):
        data.append(readdata)
        logging.info(data)
        return data, search_length
    if readdata == 0x55:
        return data, search_preamble2
    return data, search_preamble

def search_preamble(data):
    logging.info('x')
    readbyte = SER.read()
    readdata = struct.unpack("<B", readbyte)[0]
    logging.info(readdata)
    if readdata == 0x55:
        data = [0x55]
        return data, search_preamble2
    return data, search_preamble

STATE = search_preamble
data = []
while True:
    data, STATE = STATE(data)
