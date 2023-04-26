from .value import Value
import json


class Fanspeed(Value):
    _oscillation = True
    _on = True
    _mode = b"low"
    _direction_forward = True

    def set_fan_speed(self, temp):
        print("set fan", self._value)
        self._value = temp

    def fan_speed(self):
        print(self._value)
        return self._value

    def publish_state(self):
        # print("publishing" + str(self._value), str(self._oscillation))
        return (
            (self.topic_percentage_state, str(self._value).encode()),
            (
                self.topic_on_state,
                json.dumps(
                    {
                        "state": str(self._on).lower(),
                        "direction": (
                            "forward" if self._direction_forward else "reverse"
                        ),
                        "oscillation": 
                            str(self._oscillation).lower(),
                    }
                ),
            ),
            (self.topic_mode_state, self._mode),
        )

    def set_oscillation(self, temp):
        print("Set oscillation ", temp, temp == b"true")
        self._oscillation = temp == b"true"

    def set_direction(self, temp):
        print("Set direction ", temp, temp == b"true")
        self._direction_forward = temp == b"forward"

    def set_on(self, temp):
        print("Set on ", temp, temp == b"true")
        self._on = temp == b"true"

    def set_mode(self, temp):
        print("Set mode ", temp)
        self._mode = temp

    def do_subscribes(self):
        return (
            (self.topic_direction_set, lambda x: self.set_direction(x)),
            (self.topic_oscillation_set, lambda x: self.set_oscillation(x)),
            (self.topic_on_set, lambda x: self.set_on(x)),
            (self.topic_mode_state, lambda x: self.set_mode(x)),
        )

    def mqtt_config(self, zoneid):
        self.zoneid = zoneid
        self.prefix = "comfospot40_zone{}_fan".format(zoneid)
        self.topic_percentage_state = self.prefix + "/speed/percentage_state"
        self.topic_on_state = self.prefix + "/on/state"
        self.topic_on_set = self.prefix + "/on/set"
        self.topic_mode_state = self.prefix + "/preset/preset_mode_state"
        self.topic_oscillation_set = self.prefix + "/oscillation/set"
        self.topic_direction_set = self.prefix + "/direction/set"
        return {
            "name": "Comfospot40 Zone {0} Fan".format(zoneid),
            "~": self.prefix,
            "state_topic": self.topic_on_state,
            "command_topic": self.topic_on_set,
            "state_value_template": "{{ value_json.state }}",
            "direction_state_topic": self.topic_on_state,
            "direction_command_topic": self.topic_direction_set,
            "direction_value_template": "{{ value_json.direction }}",
            "oscillation_state_topic": self.topic_on_state,
            "oscillation_command_topic": self.topic_oscillation_set,
            "oscillation_value_template": "{{ value_json.oscillation }}",
            "percentage_state_topic": self.topic_percentage_state,
            "percentage_command_topic": "~/speed/percentage",
            "preset_mode_state_topic": self.topic_mode_state,
            "preset_mode_command_topic": "~/preset/preset_mode",
            "preset_modes": ["low", "mid", "high", "max"],
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
