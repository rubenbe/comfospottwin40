import asyncio
import comfospot40
import argparse

from asyncio_mqtt import Client


async def main(mqtturi, dev, oscillation_time: int, storestate):
    async with Client(mqtturi) as client:
        await client.connect()
        state = comfospot40.State()
        hal = comfospot40.Hal(state, oscillation_time)
        if storestate:
            with open(storestate, "r") as storefile:
                hal.loadState(storefile, state)
        mqtt = comfospot40.Mqtt(client, state)
        x = None
        if dev:
            await hal.setup(dev) if dev else None
            parser = hal.parser
            await mqtt.subscribe()
            x = asyncio.create_task(parser.run())
        else:
            await mqtt.subscribe()
        while True:
            mqtt.sendState(state)
            await hal.sendState(state)
            if storestate:
                with open(storestate, "w") as storefile:
                    hal.storeState(storefile, state)
            if x and x.done():
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
    parser.add_argument(
        "--state",
        action="store",
        required=False,
        help="JSON file to store state",
    )
    args = parser.parse_args()
    packetlog = None
    asyncio.run(
        main(
            mqtturi=args.mqtt,
            dev=args.dev,
            oscillation_time=args.oscillation,
            storestate=args.state,
        )
    )
