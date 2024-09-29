import av

from avi.avi import collect_packets, process_packets_for_reversal, mux_packets, close_containers


def reverse_video(input_file: str, output_file: str):
    """Reverse the video from the input file and save to the output file."""
    container = av.open(input_file)
    rev_container = av.open(output_file, "w")

    in_stream = container.streams.video[0]
    packets = collect_packets(container, in_stream)
    reversed_packets = process_packets_for_reversal(packets)

    mux_packets(rev_container, reversed_packets)
    close_containers([container, rev_container])
