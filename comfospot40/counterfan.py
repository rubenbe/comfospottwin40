from .value import Value
from comfospot40 import Fanspeed


class Counterfan(Value):
    _options = [
        "Off",
        "Always same direction",
        "Always counter direction",
        "Counter when oscillating",
    ]

    def __init__(self):
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
        return self._value != self._options[0]

    def mqtt_config(self, zoneid):
        self.zoneid = zoneid
        self.prefix = "comfospot40_zone{}_counter".format(zoneid)
        self.topic_state = self.prefix + "/state"
        self.topic_set = self.prefix + "/set"
        return {
            "name": "Comfospot40 Zone {0} Counter Fan Setting".format(zoneid),
            "state_topic": self.topic_state,
            "command_topic": self.topic_set,
            "options": self._options,
        }

    def get_fan_data(self, zonestate):
        return {"speed": zonestate.fan_speed.serial_fan_speed() if self.on() else 0}
