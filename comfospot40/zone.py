from datetime import datetime
from .temperature import Temperature
from .humidity import Humidity
from .fanspeed import Fanspeed
import json


class Zone:
    def __init__(self):
        self.inside_humidity = Humidity()
        self.inside_temperature = Temperature()
        self.recycled_humidity = Humidity()
        self.recycled_temperature = Temperature()
        self.fan_speed = Fanspeed()
        self.efficiency = None
        self.isintake = None
        self.timer = None
        self.configpublished = False

    def get_mqtt_config(self, zoneid, markpublished):
        if self.configpublished:
            return {}
        self.configpublished = markpublished
        return {
            "homeassistant/sensor/comfospot40/comfospot40_zone{}_fan/config".format(
                zoneid
            ): json.dumps(
                self.fan_speed.mqtt_config(zoneid),
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
            ): json.dumps(
                self.inside_humidity.mqtt_config(zoneid, "inside"),
            ),
            "homeassistant/sensor/comfospot40/comfospot40_zone{}_humidity_recycled/config".format(
                zoneid
            ): json.dumps(
                self.recycled_humidity.mqtt_config(zoneid, "recycled"),
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
            self.__placeholder(self.fan_speed.fan_speed(), 2),
            self.__placeholder(self.inside_temperature.temperature(), 4),
            self.__placeholder(self.inside_humidity.humidity(), 2),
            self.__placeholder(self.recycled_temperature.temperature(), 4),
            self.__placeholder(self.recycled_humidity.humidity(), 2),
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
