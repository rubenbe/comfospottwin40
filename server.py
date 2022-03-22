import asyncio
import sys
import serial
import serial_asyncio
import comfospot40
from asyncio_mqtt import Client


async def main(devicename, mqtturi, packetlog=None):
    reader, _ = await serial_asyncio.open_serial_connection(
        url=sys.argv[1], baudrate=2400, parity=serial.PARITY_NONE
    )
    async with Client(mqtturi) as client:
        parser = comfospot40.Parser(reader, packetlog)
        x = None
        while True:
            state = await parser.run()
            print(state)
            x = client.publish(
                "comfospot40/state",
                payload="online".encode(),
                qos=1,
            )
            asyncio.create_task(x)
            for zoneid, zonestate in state.zones.items():
                for topic, payloadstr in zonestate.get_mqtt_config(
                    zoneid, True
                ).items():
                    x = client.publish(
                        topic,
                        payload=payloadstr.encode(),
                        qos=1,
                    )
                    asyncio.create_task(x)
                x = client.publish(
                    "comfospot40/zones/zone{}/state".format(zoneid),
                    payload=str(getattr(zonestate, "fan_speed")).encode(),
                    qos=1,
                )
                asyncio.create_task(x)
                for attr in (
                    "fan_speed",
                    "inside_temperature",
                    "recycled_temperature",
                    "inside_humidity",
                    "recycled_humidity",
                ):
                    v = getattr(zonestate, attr)
                    v = v.value() if v and type(v) != int else v
                    x = client.publish(
                        "comfospot40/zones/zone{}/{}".format(zoneid, attr),
                        payload=str(v).encode(),
                        qos=1,
                    )
                    asyncio.create_task(x)


if __name__ == "__main__":
    assert sys.argv[1], "Please provide a serial device e.g. /dev/ttyUSB0"
    assert sys.argv[2], "Please provide a MQTT server"
    packetlog = None
    if len(sys.argv) > 3:
        packetlogname = sys.argv[3]
    asyncio.run(main(sys.argv[1], sys.argv[2], packetlog=packetlogname))
