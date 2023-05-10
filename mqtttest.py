import asyncio
import comfospot40
import sys
import argparse

from asyncio_mqtt import Client


async def main(mqtturi):
    async with Client(mqtturi) as client:
        await client.connect()
        state = comfospot40.State()
        mqtt = comfospot40.Mqtt(client, state)
        await mqtt.subscribe()
        while True:
            state.zones[1].inside_humidity.set_humidity(12)
            print("iets")
            mqtt.sendState(state)
            await asyncio.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mqtt", action="store", required=True, help="MQTT address")
    args = parser.parse_args()
    packetlog = None
    asyncio.run(main(mqtturi=args.mqtt))
