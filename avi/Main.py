import av

container = av.open("resources/lr1_1.AVI")
nextContainer = av.open("resources/lr1_2.AVI")
revContainer = av.open("resources/revers.AVI", "w")
longContainer = av.open("resources/obed2v.AVI", "w")

in_stream = container.streams.video[0]
revContainer.add_stream(template=in_stream)
longContainer.add_stream(template=in_stream)

packets = []

for packet in container.demux(in_stream):

    if packet.pts is None:
        continue

    packets.append(packet)

# packets.reverse()
# i = 0
# for packet in packets:
#     packet.pts = i
#     packet.dts = i
#     i += 1
#
# revContainer.mux(packets)
#
# packets.reverse()

for packet in nextContainer.demux(nextContainer.streams.video[0]):

    if packet.pts is None:
        continue

    packets.append(packet)

i = 0

for packet in packets:

    if packet.dts is None:
        continue

    packet.pts = i
    packet.dts = i
    i += 1

longContainer.mux(packets)

container.close()
nextContainer.close()
revContainer.close()
longContainer.close()
