from .value import Value


class Temperature(Value):
    def set_temperature(self, temp):
        self.set_value(temp)

    def temperature(self):
        return self._value

    def mqtt_config(self, mqttprefix, zoneid, name):
        self.topic_state = "{0}/zones/zone{1}/{2}_temperature".format(
            mqttprefix, zoneid, name
        )
        return {
            "name": "Comfospot40 Zone {0} {1} temperature".format(
                zoneid, name.capitalize()
            ),
            "device_class": "temperature",
            "state_class": "measurement",
            "temperature_unit": "celcius",
            "state_topic": self.topic_state,
        }

    def publish_state(self):
        return ((self.topic_state, str(self._value)),)

    def __eq__(self, other):
        return self._value == other._value
