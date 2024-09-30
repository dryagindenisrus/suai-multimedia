import av
from avi.avi import *


def reverse_video(input_file: str, output_file: str):
    """Reverse the video from the input file and save to the output file."""

    container = av.open(input_file)
    input_stream = container.streams.video[0]

    rev_container = av.open(output_file, "w")
    rev_container.add_stream(template=input_stream)

    packets = collect_packets(container, input_stream)
    reversed_packets = process_packets_for_reversal(packets)

    mux_packets(rev_container, reversed_packets)
    close_containers([container, rev_container])
