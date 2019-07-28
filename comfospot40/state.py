class Zone:
    def __init__(self):
        self.inside_humidity = None
        self.inside_temperature = None
        self.recycled_humidity = None
        self.recycled_temperature = None
        self.fan_speed = None
        self.efficiency = None
    def __placeholder(self, var, num):
        if not var:
            return '_'*num
        else:
            return var

    def __str__(self):
        return " ({})🌡️ {}C, {}% ♻️  {}C, {}%".format(
                self.__placeholder(self.fan_speed, 2),
                self.__placeholder(self.inside_temperature,4),
                self.__placeholder(self.inside_humidity,2),
                self.__placeholder(self.recycled_temperature, 4),
                self.__placeholder(self.recycled_humidity, 2))

class State:
    zones = {}
    def __init__(self):
        pass

    def addpacket(self, packet):
        if packet.hassensordata():
            zone = self.zones.get(packet.getzone(), Zone())
            print(packet.direction())
            if packet.direction() == 1:
                zone.inside_humidity=packet.humidity()
                zone.inside_temperature=packet.temperature()
            else:
                zone.recycled_humidity=packet.humidity()
                zone.recycled_temperature=packet.temperature()

            self.zones[packet.getzone()] = zone

        if packet.hasfandata():
            zone = self.zones.get(packet.getzone(), Zone())
            print(packet.direction())
            if packet.direction() == 1:
                zone.fan_speed=packet.speed()
            self.zones[packet.getzone()] = zone

    def __str__(self):
        keys = list(self.zones.keys())
        keys.sort()
        zonestr=["zone " + str(k) +": " + str(self.zones[k]) for k in keys]
        return "; ".join(zonestr);
