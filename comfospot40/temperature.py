class Temperature:
    def __init__(self):
        self._value = None

    def set_temperature(self, temp):
        self._value = temp

    def temperature(self):
        return self._value

    def value(self):
        return self._value

    def mqtt_config(self, zoneid, name):
        return {
            "name": "Comfospot40 Zone {0} {1} temperature".format(
                zoneid, name.capitalize()
            ),
            "device_class": "temperature",
            "state_class": "measurement",
            "temperature_unit": "celcius",
            "state_topic": "comfospot40/zones/zone{0}/{1}_temperature".format(
                zoneid, name
            ),
        }

    def __eq__(self, other):
        return self._value == other._value
