from .packet import Packet


def create_speed_packet(zone, intake, speed, alt=False):
    x = Packet([0] * 9)
    x.setpreamble(alt)
    x.setintake(intake)
    x.setzone(zone)
    x.setspeed(speed)
    x.setcrc()
    return x.data
