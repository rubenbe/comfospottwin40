import asyncio
import sys
import serial
import serial_asyncio
import comfospot40


async def main(devicename):
    reader, _ = await serial_asyncio.open_serial_connection(
        url=sys.argv[1], baudrate=2400, parity=serial.PARITY_NONE
    )
    parser = comfospot40.Parser(reader)
    while True:
        print("X" + str(await parser.run()))


if __name__ == "__main__":
    assert sys.argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
    asyncio.run(main(sys.argv[1]))
