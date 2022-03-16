from .packet import Packet


class CreatePacket:
    def create_speed_packet(zone, intake, speed):
        x = Packet([0] * 9)
        x.setpreamble()
        x.setintake(intake)
        x.setzone(zone)
        x.setspeed(speed)
        x.setcrc()
        return x.data
