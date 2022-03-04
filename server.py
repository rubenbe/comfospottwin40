import asyncio
import sys
import serial
import serial_asyncio
import comfospot40
from asyncio_mqtt import Client


async def main(devicename, mqtturi):
    reader, _ = await serial_asyncio.open_serial_connection(
        url=sys.argv[1], baudrate=2400, parity=serial.PARITY_NONE
    )
    async with Client(mqtturi) as client:
        parser = comfospot40.Parser(reader)
        x = None
        while True:
            state = await parser.run()
            print(state)
            for zoneid, zonestate in state.zones.items():
                x = client.publish("comfospot40/zones/zone{}/state".format(zoneid), payload=str(zonestate).encode(), qos=1)
                asyncio.create_task(x)


if __name__ == "__main__":
    assert sys.argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
    assert sys.argv[2], "Please provide a MQTT server"
    asyncio.run(main(sys.argv[1], sys.argv[2]))
