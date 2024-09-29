import av
from typing import List


def collect_packets(container, in_stream):
    """Collect video packets from the container's video stream."""
    packets = []
    for packet in container.demux(in_stream):
        if packet.pts is None:
            continue
        packets.append(packet)
    return packets


def process_packets_for_reversal(packets):
    """Prepare packets for reversal."""
    packets.reverse()
    for i, packet in enumerate(packets):
        packet.pts = i
        packet.dts = i
    return packets


def process_packets_for_long_video(packets):
    """Assign new timestamps to packets for the long video."""
    for i, packet in enumerate(packets):
        if packet.dts is None:
            continue
        packet.pts = i
        packet.dts = i
    return packets


def mux_packets(container, packets):
    """Mux packets into the specified container."""
    container.mux(packets)


def close_containers(containers):
    """Close all open video containers."""
    for container in containers:
        container.close()
