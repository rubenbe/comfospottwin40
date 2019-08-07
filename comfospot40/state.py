from datetime import datetime
from pdb import set_trace as bp

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
        if self.timer == None:
            return "   0s"
        return "{:4}s".format(int((datetime.now()-self.timer).total_seconds()))

    def __placeintake(self):
        if self.isintake == True:
            return "🏠⬅️"
        elif self.isintake == False:
            return "🏠➡️"
        else:
            return "__"

    def __placeholder(self, var, num):
        if not var:
            return '_'*num
        else:
            return var

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "{}{} ({})🌡️ {}C, {}% ♻️  {}C, {}%".format(
                self.__placeintake(),
                self.__placetimer(),
                self.__placeholder(self.fan_speed, 2),
                self.__placeholder(self.inside_temperature,4),
                self.__placeholder(self.inside_humidity,2),
                self.__placeholder(self.recycled_temperature, 4),
                self.__placeholder(self.recycled_humidity, 2))

class State:
    def __init__(self):
        self.zones = {}

    def addpacket(self, packet):
        if packet.hassensordata():
            zone = self.zones.get(packet.getzone(), Zone())
            #print(packet.direction())
            if packet.extract():
                zone.inside_humidity=packet.humidity()
                zone.inside_temperature=packet.temperature()
            else:
                zone.recycled_humidity=packet.humidity()
                zone.recycled_temperature=packet.temperature()

            self.zones[packet.getzone()] = zone

        if packet.hasfandata():
            zone = self.zones.get(packet.getzone(), Zone())
            if packet.fannumber()%2 == 0:
                oldintake = zone.isintake
                zone.isintake = packet.intake()
                if oldintake != zone.isintake:
                    zone.timer = datetime.now()
            #print(packet.direction())
            if packet.direction() == 1:
                zone.fan_speed=packet.speed()
            self.zones[packet.getzone()] = zone

    def __tozonestr(self,zone):
        if zone > 3 or zone < 1:
            return "Zone " + str(zone)
        else:
            return ('⓿','❶','❷','❸','❹','❺','❻','❼','❽','❾','❿')[zone]

    def __str__(self):
        keys = list(self.zones.keys())
        keys.sort()
        zonestr=[self.__tozonestr(k) +": " + str(self.zones[k]) for k in keys]
        return "; ".join(zonestr);
