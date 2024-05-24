from comfospot40 import Fanspeed
from .value import Value


class Counterfan(Value):
    _options = [
        b"Off",
        b"Always same direction",
        b"Always counter direction",
        b"Counter when oscillating",
    ]

    def __init__(self):
        super().__init__()
        self._value = self._options[0]

    def set_state(self, temp):
        self._value = temp

    def do_subscribes(self):
        return ((self.topic_set, lambda x: self.set_state(x)),)

    def publish_state(self):
        return ((self.topic_state, self._value),)

    def on(self):
        return self._value != self._options[0]

    def direction(self, mainfan: Fanspeed):
        forward = mainfan.direction_forward()
        if self._value == self._options[2]:
            return not forward
        if self._value == self._options[3]:
            return not forward if mainfan.oscillating() else forward
        return forward

    def mqtt_config(self, mqttprefix, zoneid):
        self.zoneid = zoneid
        self.prefix = "{0}_zone{1}_counter".format(mqttprefix, zoneid)
        self.topic_state = self.prefix + "/state"
        self.topic_set = self.prefix + "/set"
        return {
            "name": "Comfospot40 Zone {0} Counter Fan Setting".format(zoneid),
            "state_topic": self.topic_state,
            "command_topic": self.topic_set,
            "options": [x.decode("UTF-8") for x in self._options],
        }

    def get_fan_data(self, fan_speed):
        return {
            "speed": fan_speed.serial_fan_speed() if self.on() else 0,
            "direction": self.direction(fan_speed),
        }

    def toJSON(self):
        return {"state": self._value.decode("utf-8")}

    def loadJSON(self, loadedfan):
        self.set_state(loadedfan["state"].encode("UTF-8"))
