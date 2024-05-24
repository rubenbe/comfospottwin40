from .value import Value


class Humidity(Value):
    def set_humidity(self, temp):
        self.set_value(temp)

    def humidity(self):
        return self._value

    def mqtt_config(self, mqttprefix, zoneid, name):
        self.topic_state = f"{mqttprefix}/zones/zone{zoneid}/{name}_humidity"
        return {
            "name": f"Comfospot40 Zone {zoneid} {name.capitalize()} humidity",
            "device_class": "humidity",
            "state_class": "measurement",
            "temperature_unit": "percentage",
            "state_topic": self.topic_state,
        }

    def publish_state(self):
        return ((self.topic_state, str(self._value)),)

    def __eq__(self, other):
        return self._value == other._value
