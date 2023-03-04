from .value import Value


class Fanspeed(Value):
    def set_fan_speed(self, temp):
        print("set fan", self._value)
        self._value = temp

    def fan_speed(self):
        print(self._value)
        return self._value

    def mqtt_config(self, zoneid):
        return {
            "name": "Comfospot40 Zone {0} Fan".format(zoneid),
            "device_class": "humidity",
            "state_class": "measurement",
            "temperature_unit": "percentage",
            "icon": "mdi:fan",
            "state_topic": "comfospot40/zones/zone{0}/fan_speed".format(zoneid),
            # "state_topic": "comfospot40/zones/zone{0}/state".format(zoneid),
            # "percentage_state_topic": "comfospot40/zones/zone{0}/fan_speed".format(
            #    zoneid
            # ),
            # "percentage_command_topic": "comfospot40/zones/zone{0}/fan_speed_todo".format(
            #    zoneid
            # ),
            # "command_topic": "comfospot40/zones/zone{0}/set_fan_speed".format(zoneid),
        }

    def __eq__(self, other):
        return self._value == other._value
