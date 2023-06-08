from datetime import datetime
from .zone import Zone
import json


class State:
    def __init__(self):
        self.zones = {1: Zone(), 2: Zone(), 3: Zone()}

    def addpacket(self, packet):
        if packet.hassensordata():
            zone = self.zones.get(packet.getzone(), Zone())
            # print(packet.direction())
            if packet.extract():
                zone.inside_humidity.set_humidity(packet.humidity())
                zone.inside_temperature.set_temperature(packet.temperature())
            else:
                zone.recycled_humidity.set_humidity(packet.humidity())
                zone.recycled_temperature.set_temperature(packet.temperature())

            self.zones[packet.getzone()] = zone

        if packet.hasfandata():
            zone = self.zones.get(packet.getzone(), Zone())
            if packet.fannumber() % 2 == 0:
                oldintake = zone.isintake
                zone.isintake = packet.intake()
                if oldintake != zone.isintake:
                    zone.timer = datetime.now()
            # print(packet.direction())
            if packet.direction() == 1:
                zone.fan_speed.set_fan_speed(packet.speed())
            self.zones[packet.getzone()] = zone

    def set_time(self, timer: float):
        for _, zone in self.zones.items:
            zone.set_time(timer)

    def __tozonestr(self, zone):
        if zone > 3 or zone < 1:
            return "Zone " + str(zone)
        return ("⓿", "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾", "❿")[zone]

    def __str__(self):
        keys = list(self.zones.keys())
        keys.sort()
        zonestr = [self.__tozonestr(k) + ": " + str(self.zones[k]) for k in keys]
        return "; ".join(zonestr)

    def __eq__(self, other):
        if len(self.zones) != len(other.zones):
            return False
        for zone, ozone in zip(self.zones.values(), other.zones.values()):
            if zone != ozone:
                return False
        return True

    def toJSON(self):
        return {"v1": dict([(zoneid, zonestate.toJSON()) for zoneid, zonestate in self.zones.items()])}
