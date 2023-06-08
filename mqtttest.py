import asyncio
import comfospot40
import argparse

from asyncio_mqtt import Client


async def main(mqtturi, dev, oscillation_time: int):
    async with Client(mqtturi) as client:
        await client.connect()
        state = comfospot40.State()
        hal = comfospot40.Hal(state, oscillation_time)
        mqtt = comfospot40.Mqtt(client, state)
        await hal.setup(dev) if dev else None
        parser = hal.parser
        await mqtt.subscribe()
        x = asyncio.create_task(parser.run())
        while True:
            # state.zones[1].inside_humidity.set_humidity(12)
            print("iets")
            mqtt.sendState(state)
            await hal.sendState(state) if dev else None
            if x.done():
                print("DONE!")
                state = x.result()
                print(state)
                x = asyncio.create_task(parser.run())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mqtt", action="store", required=True, help="MQTT address")
    parser.add_argument("--dev", action="store", required=False, help="Serial device")
    parser.add_argument(
        "--oscillation",
        action="store",
        required=False,
        help="Oscillation time in seconds",
        default=60,
        type=int,
    )
    args = parser.parse_args()
    packetlog = None
    asyncio.run(
        main(mqtturi=args.mqtt, dev=args.dev, oscillation_time=args.oscillation)
    )
