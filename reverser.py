packets = [
    "555300980501022F0119C4",
    "5553009805010211020CEE",
    "555300980501024400E1E8",
    "555300980501023e00F0DF",
    "55530098050101370109CD",
    "5553009805010137010ACC",
]  # Sensor

packets += [
    "554D00960301020017",
    "554D00960300010019",
    "554D00970301020016",
    "554D00970300010018",
]  # Niveau 0 out?
packets += [
    "554D009603010219FE",
    "554D00960300011BFE",
    "554D00970300011BFD",
    "554D009703010219FD",
]  # Niveau 1 out
packets += [
    "554D00970301022CEA",
    "554D00960300012FEA",
    "554D00960301022CEB",
    "554D00970300012FE9",
]  # Niveau 2 out
packets += [
    "554D00960301025DBA",
    "554D009603000163B6",
    "554D009703000163B5",
    "554D00970301025DB9",
]  # Niveau 4 out
packets += [
    "554D00960301023CDB",
    "554D00960300014ECB",
    "554D00970301023CDA",
    "554D00970300014ECA",
]  # Niveau 3 out


def function1(data, offset):
    acc = offset
    for i, x in enumerate(data):
        # Some zeros seem to adjust the checksum,
        # Use the simplest theory based on the index.
        # It's currently unclear why other zeros don't adjust the checksum.
        if x == 0:
            if i == 7:
                acc -= 1
            if i == 8:
                acc += 1
        else:
            acc -= x
    acc %= 0xFF
    return acc


for offset in range(0, 0x100):
    for packet in packets:
        assert len(packet) % 2 == 0
        # print(packet)
        msb = packet[::2]
        lsb = packet[1::2]
        packetbytes = [int("".join(x), 16) for x in zip(msb, lsb)]

        packetdata = packetbytes[0:-1]
        crc = packetbytes[-1]
        if crc == function1(packetdata, offset):
            print("✔️ ", " ".join(["%02x" % i for i in packetbytes + [offset]]))
