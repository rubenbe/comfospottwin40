import asyncio
import comfospot40
import argparse

from asyncio_mqtt import Client


async def main(mqtturi, dev):
    async with Client(mqtturi) as client:
        await client.connect()
        state = comfospot40.State()
        mqtt = comfospot40.Mqtt(client, state)
        hal = comfospot40.Hal()
        await hal.setup(dev) if dev else None
        await mqtt.subscribe()
        while True:
            state.zones[1].inside_humidity.set_humidity(12)
            print("iets")
            mqtt.sendState(state)
            await hal.sendState(state) if dev else None
            await asyncio.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mqtt", action="store", required=True, help="MQTT address")
    parser.add_argument("--dev", action="store", required=False, help="Serial device")
    args = parser.parse_args()
    packetlog = None
    asyncio.run(main(mqtturi=args.mqtt, dev=args.dev))
