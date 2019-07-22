class Packet:
    def __init__(self, data):
        self.data = data

    def calculatecrc(self, data, offset=0x57):
        acc = offset
        for i, x in enumerate(data):
            #Some zeros seem to adjust the checksum,
            #Use the simplest theory based on the index.
            #It's currently unclear why other zeros don't adjust the checksum.
            if x==0:
                if i==7:
                    acc-=1
                if i==8:
                    acc+=1
            else:
                acc-=x
        acc%=0xff
        return acc
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
    def fannumber(self):
        return self.data[5]
    def direction(self):
        return self.data[6]
    def checkcrc(self):
        return self.calculatecrc(self.data) == 0
