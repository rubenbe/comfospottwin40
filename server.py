#!/usr/bin/python
import asyncio
import comfospot40
import argparse
import time
from os import path

from aiomqtt import Client


async def main(mqtturi, dev, oscillation_time: int, storestate, sensorvalidity: int):
    async with Client(mqtturi) as client:
        await client.connect()
        state = comfospot40.State(sensorvalidity)
        hal = comfospot40.Hal(state, oscillation_time)
        if storestate and path.isfile(storestate):
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
        last_print = 0
        while True:
            mqtt.sendState(state)
            new_print = time.monotonic()
            await hal.sendState(state, new_print)
            if storestate:
                with open(storestate, "w") as storefile:
                    hal.storeState(storefile, state)
            if x and x.done():
                state = x.result()
                x = asyncio.create_task(parser.run())
            if new_print - last_print > 1:
                last_print = new_print
                print(state)


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
        "--sensorvalidity",
        action="store",
        required=False,
        help="Sensor data validity in seconds",
        default=70,
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
            sensorvalidity=args.sensorvalidity,
        )
    )
