class Humidity:
    def __init__(self):
        self.value = None

    def set_humidity(self, temp):
        self.value = temp

    def humidity(self):
        return self.value

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
            "command_topic": "comfospot40/zones/zone{0}/disabled".format(zoneid),
        }

    def __eq__(self, other):
        return self.value == other.value
