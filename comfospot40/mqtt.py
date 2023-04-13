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
                x = v.publish_state()
                if not x: continue
                print("Create tasks", x)
                for publish_topic, publish_payload in x:
                    task = asyncio.create_task(self._client.publish(publish_topic, payload=publish_payload, qos=1))
                    self.background_tasks.add(task)
                    task.add_done_callback(self.background_tasks.discard)
