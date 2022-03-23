class Fanspeed:
    def __init__(self):
        self._value = None

    def set_fanspeed(self, temp):
        self._value = temp

    def fanspeed(self):
        return self._value

    def value(self):
        return self._value

    def mqtt_config(self, zoneid):
        return {
            "name": "Comfospot40 Zone {0}".format(zoneid),
            "device_class": "fan",
            "state_topic": "comfospot40/zones/zone{0}/state".format(zoneid),
            "percentage_state_topic": "comfospot40/zones/zone{0}/fan_speed".format(
                zoneid
            ),
            "percentage_command_topic": "comfospot40/zones/zone{0}/fan_speed_todo".format(
                zoneid
            ),
            "command_topic": "comfospot40/zones/zone{0}/set_fan_speed".format(zoneid),
        }

    def __eq__(self, other):
        return self._value == other._value
