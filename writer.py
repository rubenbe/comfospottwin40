#!/bin/env python
from sys import argv
from time import sleep
import asyncio
import serial_asyncio
import serial

assert argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
assert argv[2], "Please provide a zone (1-3)"
assert 0 < int(argv[2]) < 4, "Please provide a zone (1-3)"


async def main(argv):
    reader, writer = await serial_asyncio.open_serial_connection(
        url=argv[1], baudrate=2400, parity=serial.PARITY_NONE
    )

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
    print(" ".join([hex(i) for i in packet]))
    while True:
        writer.write(bytes(packet))
        print("writing")
        await asyncio.sleep(1)


asyncio.run(main(argv))
