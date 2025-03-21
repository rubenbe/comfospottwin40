#!/usr/bin/env python
import asyncio
import argparse
import time
import ssl
from os import path
from aiomqtt import Client
import comfospot40


# pylint: disable=too-many-arguments,too-many-locals


async def main(
    mqtturi,
    mqttport,
    mqttprefix,
    args,
    dev,
    oscillation_time: int,
    storestate,
    sensorvalidity: int,
    reverse: bool,
    delay: int,
):
    async with Client(
        mqtturi, port=mqttport, username=args.mqtt_username, password=args.mqtt_password
    ) as client:
        if args.mqtt_ssl:
            tls_version = ssl.PROTOCOL_TLS
            if args.mqtt_cafile:
                client.tls_set(ca_certs=args.mqtt_cafile, tls_version=tls_version)
            if args.mqtt_certfile and args.mqtt_keyfile:
                client.tls_set(
                    certfile=args.mqtt_certfile,
                    keyfile=args.mqtt_keyfile,
                    cert_reqs=ssl.CERT_NONE,
                    tls_version=tls_version,
                )

        await client.connect()
        state = comfospot40.State(sensorvalidity, reverse)
        hal = comfospot40.Hal(state, oscillation_time)
        if storestate and path.isfile(storestate):
            with open(storestate, "r", encoding="utf-8") as storefile:
                hal.load_state(storefile, state)
        mqtt = comfospot40.Mqtt(client, state, mqttprefix)
        x = None
        if dev:
            await hal.setup(dev)
            dataparser = hal.parser
            await mqtt.subscribe()
            x = asyncio.create_task(dataparser.run())
        else:
            await mqtt.subscribe()
        last_print = 0
        while True:
            mqtt.send_state(state)
            new_print = time.monotonic()
            await hal.send_state(state, new_print)
            if storestate:
                with open(storestate, "w", encoding="utf-8") as storefile:
                    hal.store_state(storefile, state)
            if x and x.done():
                state = x.result()
                x = asyncio.create_task(dataparser.run())
            if new_print - last_print > 1:
                last_print = new_print
                print(state)
            await asyncio.sleep(delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--mqtt", action="store", required=True, help="MQTT address")
    parser.add_argument(
        "--mqtt-port",
        action="store",
        required=False,
        help="MQTT port",
        default=1883,
        type=int,
    )
    parser.add_argument(
        "--mqtt-prefix",
        action="store",
        required=False,
        help="MQTT prefix",
        default="comfospot40",
    )
    parser.add_argument(
        "--mqtt-username",
        type=str,
        default=None,
        help="Username for MQTT broker authentication",
    )
    parser.add_argument(
        "--mqtt-password",
        type=str,
        default=None,
        help="Password for MQTT broker authentication",
    )
    parser.add_argument(
        "--mqtt-client-id", type=str, default="", help="Client ID for MQTT connection"
    )
    parser.add_argument(
        "--mqtt-ssl", action="store_true", help="Enable SSL/TLS for MQTT connection"
    )
    parser.add_argument(
        "--mqtt-cafile",
        type=str,
        default=None,
        help="CA file for SSL/TLS connection (optional)",
    )
    parser.add_argument(
        "--mqtt-certfile",
        type=str,
        default=None,
        help="Client certificate file for SSL/TLS connection (optional)",
    )
    parser.add_argument(
        "--mqtt-keyfile",
        type=str,
        default=None,
        help="Client private key file for SSL/TLS connection (optional)",
    )
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
        "--delay",
        action="store",
        required=False,
        choices=range(0, 31),
        help="Delay the operations on the bus (in seconds)",
        default=1,
        type=int,
    )
    parser.add_argument(
        "--state",
        action="store",
        required=False,
        help="JSON file to store state",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        required=False,
        help="Fans are installed reversed",
        default=False,
    )
    parsed_args = parser.parse_args()
    asyncio.run(
        main(
            mqtturi=parsed_args.mqtt,
            mqttport=parsed_args.mqtt_port,
            mqttprefix=parsed_args.mqtt_prefix,
            args=parsed_args,
            dev=parsed_args.dev,
            oscillation_time=parsed_args.oscillation,
            storestate=parsed_args.state,
            sensorvalidity=parsed_args.sensorvalidity,
            reverse=parsed_args.reverse,
            delay=parsed_args.delay,
        )
    )
