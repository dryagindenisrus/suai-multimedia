import av
from typing import List

from avi.avi import collect_packets, process_packets_for_long_video, close_containers, mux_packets


def combine_videos(input_files: List[str], output_file: str):
    """Combine video files into one long video."""

    containers = []
    for container in input_files:
        current_container = av.open(container)
        containers.append(current_container)

    try:
        in_stream = containers[0].streams.video[0]
    except Exception:
        raise Exception('Error while reading inputs file(s)')

    long_container = av.open(output_file, "w")
    long_container.add_stream(template=in_stream)

    packets = []
    for container in containers:
        packets.extend(collect_packets(container, in_stream))

    long_video_packets = process_packets_for_long_video(packets)

    mux_packets(long_container, long_video_packets)
    close_containers([*containers, long_container])
