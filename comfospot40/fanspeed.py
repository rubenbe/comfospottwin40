import json
import time
from .value import Value


class Fanspeed(Value):
    _oscillation = True
    _on = True
    _presets = {"low": 27, "mid": 47, "high": 78, "max": 100}
    _preset = None
    _direction_forward = True
    zoneid = None
    prefix = None
    topic_on_set = None
    topic_oscillation_set = None
    topic_direction_set = None
    topic_percentage_set = None
    topic_preset_set = None

    def __init__(self):
        super().__init__()
        self._rev_presets = dict([reversed(i) for i in self._presets.items()])
        self.set_preset(b"low")
        self._last_switched = time.monotonic()

    def set_fan_speed(self, temp):
        new_value = int(temp)
        if new_value < 10:
            self._on = False
            return
        if 0 < new_value < 27:
            new_value = 27
        self._value = new_value
        if new_value in self._rev_presets:
            self._preset = self._rev_presets[new_value]
        else:
            self._preset = "custom"

    def fan_speed(self) -> int:
        return self._value

    def serial_fan_speed(self) -> int:
        return self.fan_speed() if self._on else 0

    def on(self) -> bool:
        return self._on

    def direction_forward(self) -> bool:
        return self._direction_forward

    def maybe_switch_direction(self):
        if self._oscillation:
            self._direction_forward = not self._direction_forward
            self._last_switched = time.monotonic()

    def publish_state(self):
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

    def preset(self) -> str:
        return self._preset

    def oscillating(self):
        return self._oscillation

    def set_oscillation(self, temp):
        self._oscillation = temp == b"true"

    def set_direction(self, temp):
        old_direction = self._direction_forward
        self._direction_forward = temp == b"forward"
        if old_direction != self._direction_forward:
            self._last_switched = time.monotonic()

    def last_switched(self):
        return self._last_switched

    def set_on(self, temp):
        self._on = temp == b"true"

    def set_preset(self, temp) -> None:
        new_preset = temp.decode("UTF-8")
        if self._preset != new_preset:
            self._preset = new_preset
            for p_name, p_value in self._presets.items():
                if self._preset == p_name:
                    self.set_fan_speed(p_value)

    def do_subscribes(self):
        return (
            (self.topic_direction_set, self.set_direction),
            (self.topic_oscillation_set, self.set_oscillation),
            (self.topic_on_set, self.set_on),
            (self.topic_preset_set, self.set_preset),
            (self.topic_percentage_set, self.set_fan_speed),
        )

    def mqtt_config(self, mqttprefix, zoneid):
        self.zoneid = zoneid
        self.prefix = f"{mqttprefix}_zone{zoneid}_fan"
        self.topic_state = self.prefix + "/state"
        self.topic_on_set = self.prefix + "/on/set"
        self.topic_oscillation_set = self.prefix + "/oscillation/set"
        self.topic_direction_set = self.prefix + "/direction/set"
        self.topic_percentage_set = self.prefix + "/speed/percentage"
        self.topic_preset_set = self.prefix + "/preset/set"
        mqtt_preset_modes = list(self._presets.keys())
        mqtt_preset_modes.append("custom")
        return {
            "name": f"Comfospot40 Zone {zoneid} Fan",
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
            "preset_modes": mqtt_preset_modes,
            "qos": 0,
            "payload_on": "true",
            "payload_off": "false",
            "payload_oscillation_on": "true",
            "payload_oscillation_off": "false",
            "unique_id": f"{mqttprefix}_zone{zoneid}_fan",
        }

    def __eq__(self, other):
        return self._value == other._value

    def to_json(self):
        return {
            "on": self.on(),
            "speed": self.fan_speed(),
            "forward": self.direction_forward(),
            "oscillation": self.oscillating(),
        }

    def load_json(self, loadedfan):
        self._on = loadedfan["on"]
        self._oscillation = loadedfan["oscillation"]
        self._direction_forward = loadedfan["forward"]
        self.set_fan_speed(loadedfan["speed"])
