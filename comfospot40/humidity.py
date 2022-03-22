class Humidity:
    def __init__(self):
        self._value = None

    def set_humidity(self, temp):
        self._value = temp

    def humidity(self):
        return self._value

    def value(self):
        return self._value

    def mqtt_config(self, zoneid, name):
        return {
            "name": "Comfospot40 Zone {0} {1} humidity".format(
                zoneid, name.capitalize()
            ),
            "device_class": "humidity",
            "state_class": "measurement",
            "temperature_unit": "percentage",
            "state_topic": "comfospot40/zones/zone{0}/{1}_humidity".format(
                zoneid, name
            ),
        }

    def __eq__(self, other):
        return self._value == other._value
