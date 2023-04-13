from .value import Value


class Fanspeed(Value):
    def set_fan_speed(self, temp):
        print("set fan", self._value)
        self._value = temp

    def fan_speed(self):
        print(self._value)
        return self._value

    def publish_state(self):
        print("publishing" + str(self._value))
        return (
            (self.topic_percentage_state, str(self._value).encode()),
            (self.topic_oscillation_state + "/oscillation/state", str("true").encode()),
            (self.topic_on_state, str("true").encode()),
            (self.topic_mode_state, str("out").encode()),
        )

    def mqtt_config(self, zoneid):
        self.zoneid = zoneid
        self.prefix = "comfospot40_zone{}_fan".format(zoneid)
        self.topic_percentage_state = self.prefix + "/speed/percentage_state"
        self.topic_on_state = self.prefix + "/on/state"
        self.topic_mode_state = self.prefix + "/preset/preset_mode_state"
        self.topic_oscillation_state = self.prefix + "/oscillation/state"
        return {
            "name": "Comfospot40 Zone {0} Fan".format(zoneid),
            "~": self.prefix,
            "state_topic": self.topic_on_state,
            "command_topic": "~/on/set",
            "oscillation_state_topic": self.topic_oscillation_state,
            "oscillation_command_topic": "~/oscillation/set",
            "percentage_state_topic": self.topic_percentage_state,
            "percentage_command_topic": "~/speed/percentage",
            "preset_mode_state_topic": self.topic_mode_state,
            "preset_mode_command_topic": "~/preset/preset_mode",
            "preset_modes": ["in", "out", "in low", "low", "mid", "high", "max"],
            "qos": 0,
            "payload_on": "true",
            "payload_off": "false",
            "payload_oscillation_on": "true",
            "payload_oscillation_off": "false",
            "speed_range_min": 16,
            "speed_range_max": 128,
            "unique_id": "comfospot40_zone{}_fan".format(zoneid),
        }

    def __eq__(self, other):
        return self._value == other._value
