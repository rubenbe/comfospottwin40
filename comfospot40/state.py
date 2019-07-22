class Zone:
    def __init__(self):
        self.inside_humidity = None
        self.inside_temperature = None
        self.recycled_humidity = None
        self.recycled_temperature = None
        self.fanspeed = None
        self.efficiency = None

    def __str__(self):
        return "Inside {}C, {}% Recycled {}C, {}%".format(
                self.inside_temperature, self.inside_humidity,
                self.recycled_temperature, self.recycled_humidity)

class State:
    zones = {}
    def __init__(self):
        pass

    def addpacket(self, packet):
        if(packet.hassensordata):
            zone = self.zones.get(packet.getzone(), Zone())
            print(packet.direction())
            if packet.direction() == 1:
                zone.inside_humidity=packet.humidity()
                zone.inside_temperature=packet.temperature()
            else:
                zone.recycled_humidity=packet.humidity()
                zone.recycled_temperature=packet.temperature()

            self.zones[packet.getzone()] = zone
    def __str__(self):
        zonestr=["zone " + str(k) +": " + str(z) for k, z in self.zones.items()]
        return "; ".join(zonestr);
