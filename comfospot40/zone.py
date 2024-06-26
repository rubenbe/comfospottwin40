import json
from .temperature import Temperature
from .humidity import Humidity
from .fanspeed import Fanspeed
from .counterfan import Counterfan


class Zone:
    def __init__(self, sensorvalidity=None):
        self.inside_humidity = Humidity(sensorvalidity)
        self.inside_temperature = Temperature(sensorvalidity)
        self.recycled_humidity = Humidity(sensorvalidity)
        self.recycled_temperature = Temperature(sensorvalidity)
        self.fan_speed = Fanspeed()
        self.counter_fan = Counterfan()
        self.efficiency = None
        self.isintake = None
        self.timer = None
        self.configpublished = False
        self._sensorvalidity = sensorvalidity

    def set_time(self, timer):
        self.timer = timer - self.fan_speed.last_switched()
        self.inside_humidity.set_time(timer)
        self.inside_temperature.set_time(timer)
        self.recycled_humidity.set_time(timer)
        self.recycled_temperature.set_time(timer)

    def maybe_switch_direction(self):
        self.fan_speed.maybe_switch_direction()

    def get_mqtt_config(self, mqttprefix, zoneid, markpublished):
        if self.configpublished:
            return {}
        self.configpublished = markpublished
        return {
            f"homeassistant/select/{mqttprefix}_zone{zoneid}_counter/config": json.dumps(  # noqa: E501  # pylint: disable=line-too-long
                self.counter_fan.mqtt_config(mqttprefix, zoneid),
            ),
            f"homeassistant/fan/{mqttprefix}_zone{zoneid}_fan/config": json.dumps(
                self.fan_speed.mqtt_config(mqttprefix, zoneid),
            ),
            f"homeassistant/sensor/{mqttprefix}/{mqttprefix}_zone{zoneid}_temp_in/config": json.dumps(  # noqa: E501  # pylint: disable=line-too-long
                self.inside_temperature.mqtt_config(mqttprefix, zoneid, "inside"),
            ),
            f"homeassistant/sensor/{mqttprefix}/{mqttprefix}_zone{zoneid}_temp_recycled/config": json.dumps(  # noqa: E501  # pylint: disable=line-too-long
                self.recycled_temperature.mqtt_config(mqttprefix, zoneid, "recycled"),
            ),
            f"homeassistant/sensor/{mqttprefix}/{mqttprefix}_zone{zoneid}_humidity_in/config": json.dumps(  # noqa: E501  # pylint: disable=line-too-long
                self.inside_humidity.mqtt_config(mqttprefix, zoneid, "inside"),
            ),
            f"homeassistant/sensor/{mqttprefix}/{mqttprefix}_zone{zoneid}_humidity_recycled/config": json.dumps(  # noqa: E501  # pylint: disable=line-too-long
                self.recycled_humidity.mqtt_config(mqttprefix, zoneid, "recycled"),
            ),
        }

    def __placetimer(self):
        if self.timer is None:
            return "   0s"
        return f"{int(self.timer):4}s"

    def __place_oscillation(self):
        if self.fan_speed.oscillating():
            return "🔀"
        return "  "

    def __placeintake(self):
        if not self.fan_speed.on():
            return "🏠⏸️"
        if self.fan_speed.direction_forward():
            return "🏠➡️"
        return "🏠⬅️"

    def __placecounterintake(self):
        if not self.counter_fan.on() or not self.fan_speed.on():
            return "⏸️"
        if self.counter_fan.direction(self.fan_speed):
            return "➡️"
        return "⬅️"

    def __placeholder(self, var, num):
        if not var:
            return "_" * num
        if isinstance(var, str):
            return var[0:num]
        return var

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
            f"{self.__place_oscillation()}{self.__placeintake()}"
            " "
            f"{self.__placecounterintake()}{self.__placetimer()}"
            " ("
            f"{self.__placeholder(self.fan_speed.fan_speed(), 2)}"
            " "
            f"{self.__placeholder(self.fan_speed.preset(), 2)}"
            ")🌡️ "
            f"{self.__placeholder(self.inside_temperature.temperature(), 4)}"
            "C, "
            f"{self.__placeholder(self.inside_humidity.humidity(), 2)}"
            "% ♻️  "
            f"{self.__placeholder(self.recycled_temperature.temperature(), 4)}"
            "C, "
            f"{self.__placeholder(self.recycled_humidity.humidity(), 2)}"
            "%"
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

    def to_json(self):
        return {
            "fan": self.fan_speed.to_json(),
            "counterfan": self.counter_fan.to_json(),
        }

    def load_json(self, loadedzone):
        self.fan_speed.load_json(loadedzone["fan"])
        self.counter_fan.load_json(loadedzone["counterfan"])
