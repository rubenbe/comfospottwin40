import asyncio
from aiomqtt import Client
import comfospot40


class Mqtt:
    background_tasks = set()
    topics = []

    def __init__(self, client: Client, state: comfospot40.State, mqttprefix: str):
        self._client = client
        client.pending_calls_threshold = 20
        self._state = state
        self.send_config(mqttprefix)

    def send_config(self, mqttprefix):
        for zoneid, zonestate in self._state.zones.items():
            for topic, payloadstr in zonestate.get_mqtt_config(
                mqttprefix, zoneid, True
            ).items():
                x = self._client.publish(
                    topic,
                    payload=payloadstr.encode(),
                    qos=1,
                    retain=True,
                )
                task = asyncio.create_task(x)
                self.background_tasks.add(task)
                task.add_done_callback(self.background_tasks.discard)

    async def listen(self):
        async with self._client.messages() as messages:
            async for message in messages:
                for topic_name, topic_callback in self.topics:
                    if topic_name == str(message.topic):
                        topic_callback(message.payload)

    async def subscribe(self):
        task = asyncio.create_task(self.listen())
        self.background_tasks.add(task)
        task.add_done_callback(self.background_tasks.discard)
        self.topics = []
        for _, zonestate in self._state.zones.items():
            for attr in (
                "inside_temperature",
                "recycled_temperature",
                "inside_humidity",
                "recycled_humidity",
                "fan_speed",
                "counter_fan",
            ):
                v = getattr(zonestate, attr)
                x = v.do_subscribes()
                if not x:
                    continue
                print("Subscribe", x)
                for subscribe_topic, subscribe_callback in x:
                    print("Subscribe", subscribe_topic)
                    await self._client.subscribe(subscribe_topic)
                    self.topics.append((subscribe_topic, subscribe_callback))

    def send_state(self, state):
        for _, zonestate in state.zones.items():
            for attr in (
                "inside_temperature",
                "recycled_temperature",
                "inside_humidity",
                "recycled_humidity",
                "fan_speed",
                "counter_fan",
            ):
                v = getattr(zonestate, attr)
                x = v.publish_state()
                if not x:
                    continue
                # print("Create tasks", x)
                for publish_topic, publish_payload in x:
                    task = asyncio.create_task(
                        self._client.publish(
                            publish_topic, payload=publish_payload, qos=1
                        )
                    )
                    self.background_tasks.add(task)
                    task.add_done_callback(self.background_tasks.discard)
