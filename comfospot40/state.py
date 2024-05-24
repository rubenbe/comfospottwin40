from datetime import datetime
from .zone import Zone


class State:
    def __init__(self, sensorvalidity: int = None, reverse: bool = False):
        self.zones = {
            1: Zone(sensorvalidity),
            2: Zone(sensorvalidity),
            3: Zone(sensorvalidity),
        }
        self.reverse = reverse

    def addpacket(self, packet):
        if packet.hassensordata():
            zone = self.zones.get(packet.getzone(), Zone())
            # print(packet.direction())
            if packet.extract() != self.reverse:
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

    def from_json(self, loadedjson):
        if "v1" in loadedjson:
            # print("ok")
            loadedzones = loadedjson["v1"]
            for zoneid, loadedzone in loadedzones.items():
                # print("todo", zoneid, loadedzone)
                self.zones[int(zoneid)].load_json(loadedzone)

    def to_json(self):
        return {
            "v1": dict(
                [
                    (zoneid, zonestate.to_json())
                    for zoneid, zonestate in self.zones.items()
                ]
            )
        }
