from datetime import datetime
from .temperature import Temperature
import json


class Zone:
    def __init__(self):
        self.inside_humidity = None
        self.inside_temperature = Temperature()
        self.recycled_humidity = None
        self.recycled_temperature = Temperature()
        self.fan_speed = None
        self.efficiency = None
        self.isintake = None
        self.timer = None
        self.configpublished = False

    def get_mqtt_config(self, zoneid, markpublished):
        if self.configpublished:
            return {}
        self.configpublished = markpublished
        return {
            "homeassistant/fan/comfospot40/comfospot40_zone{}/config".format(
                zoneid
            ): """{{
                        "name": "Comfospot40 Zone {0}",
                        "device_class": "fan",
                        "state_topic": "comfospot40/zones/zone{0}/state",
                        "percentage_state_topic": "comfospot40/zones/zone{0}/fan_speed",
                        "percentage_command_topic": "comfospot40/zones/zone{0}/fan_speed_todo",
                        "command_topic": "comfospot40/zones/zone{0}/set_fan_speed"}}""".format(
                zoneid
            ),
            "homeassistant/sensor/comfospot40/comfospot40_zone{}_temp_in/config".format(
                zoneid
            ): json.dumps(
                self.inside_temperature.mqtt_config(zoneid, "inside"),
            ),
            "homeassistant/sensor/comfospot40/comfospot40_zone{}_temp_recycled/config".format(
                zoneid
            ): json.dumps(
                self.inside_temperature.mqtt_config(zoneid, "recycled"),
            ),
            "homeassistant/sensor/comfospot40/comfospot40_zone{}_humidity_in/config".format(
                zoneid
            ): """{{
                        "name": "Comfospot40 Zone {0} Inside humidity",
                        "device_class": "humidity",
                        "state_class": "measurement",
                        "temperature_unit": "percentage",
                        "state_topic": "comfospot40/zones/zone{0}/inside_humidity",
                        "command_topic": "comfospot40/zones/zone{0}/disabled"}}""".format(
                zoneid
            ),
            "homeassistant/sensor/comfospot40/comfospot40_zone{}_humidity_recycled/config".format(
                zoneid
            ): """{{
                        "name": "Comfospot40 Zone {0} Recycled humidity",
                        "device_class": "humidity",
                        "state_class": "measurement",
                        "temperature_unit": "percentage",
                        "state_topic": "comfospot40/zones/zone{0}/recycled_humidity",
                        "command_topic": "comfospot40/zones/zone{0}/disabled"}}""".format(
                zoneid
            ),
        }

    def __placetimer(self):
        if self.timer is None:
            return "   0s"
        return "{:4}s".format(int((datetime.now() - self.timer).total_seconds()))

    def __placeintake(self):
        if self.isintake:
            return "🏠⬅️"
        if not self.isintake:
            return "🏠➡️"
        return "__"

    def __placeholder(self, var, num):
        if not var:
            return "_" * num
        return var

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}{} ({})🌡️ {}C, {}% ♻️  {}C, {}%".format(
            self.__placeintake(),
            self.__placetimer(),
            self.__placeholder(self.fan_speed, 2),
            self.__placeholder(self.inside_temperature.temperature(), 4),
            self.__placeholder(self.inside_humidity, 2),
            self.__placeholder(self.recycled_temperature.temperature(), 4),
            self.__placeholder(self.recycled_humidity, 2),
        )

    def __eq__(self, other):
        # ignore self.timer
        return (
            self.inside_humidity == other.inside_humidity
            and self.inside_temperature == other.inside_temperature
            and self.recycled_humidity == other.recycled_humidity
            and self.recycled_temperature == other.recycled_temperature
            and self.fan_speed == other.fan_speed
            and self.isintake == other.isintake
        )
