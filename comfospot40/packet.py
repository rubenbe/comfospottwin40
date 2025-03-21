class Packet:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return " ".join([f"0x{data:02x}" for data in self.data])

    def calculatecrc(self, data):
        total = sum(data)
        total = ~total + 0x56
        return total & 0xFF

    def setpreamble(self, alt=False):
        self.data[0] = 0x55
        self.data[1] = 0x4D
        self.data[2] = 0x00
        if not alt:
            self.data[3] = 0x96
        else:
            self.data[3] = 0x97
        self.data[4] = len(self.data) - 6

    def hassensordata(self):
        return self.data[3] == 0x98

    def hasfandata(self):
        return self.data[3] in (0x97, 0x96)

    def humidity(self):
        return self.data[7]

    def temperature(self):
        return (self.data[8] * 256 + self.data[9]) / 10

    def speed(self):
        return self.data[7]

    def setspeed(self, speed):
        self.data[7] = speed

    def getzone(self):
        return int(self.data[5] / 2) + 1

    def setzone(self, value):
        self.data[5] = (value - 1) * 2

    def fannumber(self):
        return self.data[5]

    def direction(self):
        return self.data[6]

    def checkcrc(self):
        return self.calculatecrc(self.data) == 0

    def setcrc(self):
        self.data[-1] = self.calculatecrc(self.data[0:-1])

    def intake(self):
        return self.direction() == 2

    def setdirectiongroup(self, group):
        self.data[5] = self.data[5] + group

    def setintake(self, isintake):
        if isintake:
            self.data[6] = 2
        else:
            self.data[6] = 1

    def extract(self):
        return not self.intake()
