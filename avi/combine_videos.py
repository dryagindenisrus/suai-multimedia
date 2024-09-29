import av
from typing import List

from avi.avi import collect_packets, process_packets_for_long_video, close_containers, mux_packets


def combine_videos(input_files: List[str], output_file: str):
    """Combine two video files into one long video."""
    container1 = av.open(input_files[0])
    container2 = av.open(input_files[1])
    long_container = av.open(output_file, "w")

    in_stream1 = container1.streams.video[0]
    packets1 = collect_packets(container1, in_stream1)

    in_stream2 = container2.streams.video[0]
    packets2 = collect_packets(container2, in_stream2)

    all_packets = packets1 + packets2
    long_video_packets = process_packets_for_long_video(all_packets)

    mux_packets(long_container, long_video_packets)
    close_containers([container1, container2, long_container])
