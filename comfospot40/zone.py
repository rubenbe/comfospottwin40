from datetime import datetime


class Zone:
    def __init__(self):
        self.inside_humidity = None
        self.inside_temperature = None
        self.recycled_humidity = None
        self.recycled_temperature = None
        self.fan_speed = None
        self.efficiency = None
        self.isintake = None
        self.timer = None

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
            self.__placeholder(self.inside_temperature, 4),
            self.__placeholder(self.inside_humidity, 2),
            self.__placeholder(self.recycled_temperature, 4),
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
