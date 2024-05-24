from asyncio import sleep
from serial_asyncio import open_serial_connection
import serial
import json
import time
import logging
from comfospot40 import State, Parser, create_packet


class Hal:
    def __init__(self, state, oscillation_time):
        self._state = state
        self._oscillation_time = oscillation_time
        self._oscillation_switch = time.monotonic()
        self._writer = None

    async def setup(self, devpath: str):
        self._reader, self._writer = await open_serial_connection(
            url=devpath, baudrate=2400, parity=serial.PARITY_NONE
        )
        self.parser = Parser(self._reader, None, self._state)

    async def send_state(self, state: State, timer):
        dirtimer = timer - self._oscillation_switch
        switch_dir = dirtimer > self._oscillation_time
        if switch_dir:
            self._oscillation_switch = timer
        for zoneid, zonestate in state.zones.items():
            fan_speed = zonestate.fan_speed.serial_fan_speed()
            zonestate.set_time(timer)
            # print(zoneid, fan_speed)
            if switch_dir:
                zonestate.maybe_switch_direction()
            packet = create_packet.create_speed_packet(
                zoneid, zonestate.fan_speed.direction_forward(), fan_speed, 0, True
            )
            self._writer.write(bytes(packet)) if self._writer else None
            await sleep(0.1)
            counter = zonestate.counter_fan.get_fan_data(zonestate.fan_speed)
            # print(counter["direction"], counter["speed"])
            packet = create_packet.create_speed_packet(
                zoneid, counter["direction"], counter["speed"], 1, True
            )
            # print("Writing")
            self._writer.write(bytes(packet)) if self._writer else None
            await sleep(0.1)

    def storeState(self, storefile, state):
        json.dump(state.toJSON(), storefile, indent=2)

    def loadState(self, storefile, state):
        try:
            loadedjson = json.load(storefile)
        except json.decoder.JSONDecodeError as e:
            logging.info("Failed to decode json {}".format(e))
            return
        logging.info(loadedjson)
        state.fromJSON(loadedjson)
