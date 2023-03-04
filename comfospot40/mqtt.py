from asyncio_mqtt import Client
import asyncio
import comfospot40


class Mqtt:
    background_tasks = set()

    def __init__(self, client: Client, state: comfospot40.State):
        self._client = client
        for zoneid, zonestate in state.zones.items():
            for topic, payloadstr in zonestate.get_mqtt_config(zoneid, True).items():
                x = client.publish(
                    topic,
                    payload=payloadstr.encode(),
                    qos=1,
                )
                task = asyncio.create_task(x)
                self.background_tasks.add(task)
                task.add_done_callback(self.background_tasks.discard)

    def sendState(self, state):
        for zoneid, zonestate in state.zones.items():
            for attr in (
                "inside_temperature",
                "recycled_temperature",
                "inside_humidity",
                "recycled_humidity",
                "fan_speed",
            ):
                v = getattr(zonestate, attr)
                v = v.value() if v else None
                x = self._client.publish(
                    "comfospot40/zones/zone{}/{}".format(zoneid, attr),
                    payload=str(v).encode(),
                    qos=1,
                )
                task = asyncio.create_task(x)
                self.background_tasks.add(task)
                task.add_done_callback(self.background_tasks.discard)
