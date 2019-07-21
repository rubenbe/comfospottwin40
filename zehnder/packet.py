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

    def checkcrc(self):
        return self.calculatecrc(self.data) == 0
