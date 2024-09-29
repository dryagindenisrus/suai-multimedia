import numpy as np
import PIL.Image
import av
from av.video.frame import VideoFrame
import pip
from matplotlib import pyplot as plt
import time
from numpy import sqrt


def output_cut_video(path_in1, path_in2, path_out):
    input_container = av.open(path_in1)
    input_container2 = av.open(path_in2)
    output_container = av.open(path_out, 'w')

    input_stream = input_container.streams.video[0]
    input_stream2 = input_container.streams.video[0]

    arr = []
    arr2 = []

    out_stream = output_container.add_stream(input_stream.codec_context.name, rate=round(input_stream.average_rate))
    out_stream.width = input_container.streams.video[0].codec_context.width
    out_stream.height = input_container.streams.video[0].codec_context.height
    out_stream.bit_rate = input_stream.bit_rate

    for packet in input_container.demux(input_stream):
        for frame in packet.decode():
            arr.append(np.array(frame.to_image()))
    arr = np.array(arr)

    for packet in input_container2.demux(input_stream2):
        for frame in packet.decode():
            arr2.append(np.array(frame.to_image()))
    arr2 = np.array(arr2)

    frames = arr
    size = len(arr) if len(arr) < len(arr2) else len(arr2)

    print(arr.shape)
    arr = arr[:, :, ::2, ]

    print(arr.shape)
    arr2 = arr2[:, :, ::2, ]

    for i in range(size):
        frames[i] = np.hstack((arr[i], arr2[i]))

    for frame in frames:
        image = av.VideoFrame.from_ndarray(frame, format='rgb24')
        for packet in out_stream.encode(image):
            output_container.mux(packet)
    output_container.close()


output_cut_video('resources/lr1_1.avi', 'resources/lr1_2.avi', 'resources/out_lr1_12.avi')
