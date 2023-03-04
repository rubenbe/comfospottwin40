import asyncio
import comfospot40
import sys

from asyncio_mqtt import Client


async def main(mqtturi):
    async with Client(mqtturi) as client:
        state = comfospot40.State()
        mqtt = comfospot40.Mqtt(client, state)
        while True:
            state.zones[1].fan_speed.set_fan_speed(23)
            state.zones[1].inside_humidity.set_humidity(12)
            print("iets")
            mqtt.sendState(state)
            await asyncio.sleep(1)


if __name__ == "__main__":
    assert sys.argv[1], "Please provide a MQTT server"
    packetlog = None
    asyncio.run(main(sys.argv[1]))
