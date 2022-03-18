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
                x = client.publish(
                    "homeassistant/fan/comfospot40/comfospot40_zone{}/config".format(
                        zoneid
                    ),
                    payload="""{{
                        "name": "Comfospot40 Zone {0}",
                        "device_class": "fan",
                        "state_topic": "comfospot40/zones/zone{0}/state",
                        "percentage_state_topic": "comfospot40/zones/zone{0}/fan_speed",
                        "percentage_command_topic": "comfospot40/zones/zone{0}/fan_speed_todo",
                        "command_topic": "comfospot40/zones/zone{0}/set_fan_speed"}}
                    """.format(
                        zoneid
                    ).encode(),
                    qos=1,
                )
                asyncio.create_task(x)
                x = client.publish(
                    "homeassistant/sensor/comfospot40/comfospot40_zone{}_temp_in/config".format(
                        zoneid
                    ),
                    payload="""{{
                        "name": "Comfospot40 Zone {0} Inside temperature",
                        "device_class": "temperature",
                        "state_class": "measurement",
                        "temperature_unit": "celcius",
                        "state_topic": "comfospot40/zones/zone{0}/inside_temperature",
                        "command_topic": "comfospot40/zones/zone{0}/disabled"}}
                    """.format(
                        zoneid
                    ).encode(),
                    qos=1,
                )
                asyncio.create_task(x)
                x = client.publish(
                    "homeassistant/sensor/comfospot40/comfospot40_zone{}_temp_recycled/config".format(
                        zoneid
                    ),
                    payload="""{{
                        "name": "Comfospot40 Zone {0} Recycled temperature",
                        "device_class": "temperature",
                        "state_class": "measurement",
                        "temperature_unit": "celcius",
                        "state_topic": "comfospot40/zones/zone{0}/recycled_temperature",
                        "command_topic": "comfospot40/zones/zone{0}/disabled"}}
                    """.format(
                        zoneid
                    ).encode(),
                    qos=1,
                )
                asyncio.create_task(x)
                x = client.publish(
                    "homeassistant/sensor/comfospot40/comfospot40_zone{}_humidity_in/config".format(
                        zoneid
                    ),
                    payload="""{{
                        "name": "Comfospot40 Zone {0} Inside humidity",
                        "device_class": "humidity",
                        "state_class": "measurement",
                        "temperature_unit": "percentage",
                        "state_topic": "comfospot40/zones/zone{0}/inside_humidity",
                        "command_topic": "comfospot40/zones/zone{0}/disabled"}}
                    """.format(
                        zoneid
                    ).encode(),
                    qos=1,
                )
                asyncio.create_task(x)
                x = client.publish(
                    "homeassistant/sensor/comfospot40/comfospot40_zone{}_humidity_recycled/config".format(
                        zoneid
                    ),
                    payload="""{{
                        "name": "Comfospot40 Zone {0} Recycled humidity",
                        "device_class": "humidity",
                        "state_class": "measurement",
                        "temperature_unit": "percentage",
                        "state_topic": "comfospot40/zones/zone{0}/recycled_humidity",
                        "command_topic": "comfospot40/zones/zone{0}/disabled"}}
                    """.format(
                        zoneid
                    ).encode(),
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
                    x = client.publish(
                        "comfospot40/zones/zone{}/{}".format(zoneid, attr),
                        payload=str(getattr(zonestate, attr)).encode(),
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
