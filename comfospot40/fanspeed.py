from .value import Value
import json


class Fanspeed(Value):
    _oscillation = True
    _on = True
    _presets = (("low", 27), ("mid", 47), ("high", 78), ("max", 99))
    _preset = None
    _direction_forward = True
    def __init__(self):
        super().__init__()
        self.set_preset(b"low")

    def set_fan_speed(self, temp):
        self._value = int(temp)
        print("set fan", self._value)

    def fan_speed(self):
        print(self._value)
        return self._value

    def publish_state(self):
        # print("publishing" + str(self._value), str(self._oscillation))
        return (
            (
                self.topic_state,
                json.dumps(
                    {
                        "state": str(self._on).lower(),
                        "direction": (
                            "forward" if self._direction_forward else "reverse"
                        ),
                        "oscillation": str(self._oscillation).lower(),
                        "percentage": str(self._value),
                        "preset": self._preset,
                    }
                ),
            ),
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

    def set_preset(self, temp) -> None:
        print("Set preset ", temp)
        new_preset = temp.decode("UTF-8")
        if self._preset != new_preset:
            self._preset = new_preset
            for p_name, p_value in self._presets:
                if self._preset == p_name:
                    self.set_fan_speed(p_value)

    def do_subscribes(self):
        return (
            (self.topic_direction_set, lambda x: self.set_direction(x)),
            (self.topic_oscillation_set, lambda x: self.set_oscillation(x)),
            (self.topic_on_set, lambda x: self.set_on(x)),
            (self.topic_preset_set, lambda x: self.set_preset(x)),
            (self.topic_percentage_set, lambda x: self.set_fan_speed(x)),
        )

    def mqtt_config(self, zoneid):
        self.zoneid = zoneid
        self.prefix = "comfospot40_zone{}_fan".format(zoneid)
        self.topic_state = self.prefix + "/state"
        self.topic_on_set = self.prefix + "/on/set"
        self.topic_oscillation_set = self.prefix + "/oscillation/set"
        self.topic_direction_set = self.prefix + "/direction/set"
        self.topic_percentage_set = self.prefix + "/speed/percentage"
        self.topic_preset_set = self.prefix + "/preset/set"
        return {
            "name": "Comfospot40 Zone {0} Fan".format(zoneid),
            "state_topic": self.topic_state,
            "command_topic": self.topic_on_set,
            "state_value_template": "{{ value_json.state }}",
            "direction_state_topic": self.topic_state,
            "direction_command_topic": self.topic_direction_set,
            "direction_value_template": "{{ value_json.direction }}",
            "oscillation_state_topic": self.topic_state,
            "oscillation_command_topic": self.topic_oscillation_set,
            "oscillation_value_template": "{{ value_json.oscillation }}",
            "percentage_state_topic": self.topic_state,
            "percentage_command_topic": self.topic_percentage_set,
            "percentage_value_template": "{{ value_json.percentage }}",
            "preset_mode_state_topic": self.topic_state,
            "preset_mode_command_topic": self.topic_preset_set,
            "preset_mode_value_template": "{{ value_json.preset }}",
            "preset_modes": ["low", "mid", "high", "max"],
            "qos": 0,
            "payload_on": "true",
            "payload_off": "false",
            "payload_oscillation_on": "true",
            "payload_oscillation_off": "false",
            "unique_id": "comfospot40_zone{}_fan".format(zoneid),
        }

    def __eq__(self, other):
        return self._value == other._value
