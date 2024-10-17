import numpy as np
import av
from av.video.frame import VideoFrame
from matplotlib import pyplot as plt
from numpy import sqrt
import matplotlib

last_height = None
last_width = None
last_numb_frames = None


def input_video(path, reformat_name=None):
    """Returns video as a list of frames as numpy arrays."""
    global last_height, last_width, last_numb_frames
    array_list = []
    input_container = av.open(path)

    format_container_name = input_container.format.name
    codec_name = input_container.streams.video[0].codec_context.name
    frame_width = input_container.streams.video[0].codec_context.width
    frame_height = input_container.streams.video[0].codec_context.height
    rate = input_container.streams.video[0].average_rate
    format_frame_name = input_container.streams.video[0].codec_context.format.name

    last_height = frame_height
    last_width = frame_width
    last_numb_frames = input_container.streams.video[0].frames

    if reformat_name is None:
        reformat_name = format_frame_name

    for frame in input_container.decode(video=0):
        frame = frame.reformat(frame_width, frame_height, reformat_name)
        array = frame.to_ndarray()
        array_list.append(array)

    input_container.close()
    return array_list, format_container_name, reformat_name, codec_name, rate


def output_video(path, array_list, format_container_name, format_frame_name, codec_name, rate):
    """Writes the processed video frames to the output file."""
    output_container = av.open(path, mode='w')
    output_stream = output_container.add_stream(codec_name, rate=rate)
    output_stream.height = 120
    output_stream.width = 176

    for array in array_list:
        frame = VideoFrame.from_ndarray(array.astype(np.uint8), format=format_frame_name)
        frame2 = output_stream.encode(frame)
        output_container.mux(frame2)

    output_container.close()


def autocorrelation(Y_array, width, height, quantity_frames):
    """Calculates the autocorrelation of the given array."""
    print(f"Autocorrelation start working, data:\nwidth: {width}\nheight: {height}\nquantity_frames: {quantity_frames}")

    K = width * height
    offset = -quantity_frames + 1
    list_R = []

    while offset < quantity_frames:
        # Create copies of the original array
        Y1 = Y_array.copy()
        Y2 = Y_array.copy()

        if offset > 0:
            Y1 = Y1[int(K) * offset:]  # Remove leading elements from Y1
            Y2 = Y2[:-int(K) * offset]  # Remove trailing elements from Y2
        elif offset < 0:
            Y1 = Y1[:-int(K) * abs(offset)]  # Remove trailing elements from Y1
            Y2 = Y2[int(K) * abs(offset):]  # Remove leading elements from Y2

        # Ensure both arrays are of the same length for correlation calculation
        min_length = min(len(Y1), len(Y2))
        if min_length == 0:
            list_R.append(0)  # Append a default value if arrays are empty
            print(f"Warning: One of the arrays is empty after offset adjustment for offset {offset}.")
            offset += 1
            continue

        # Trim both arrays to the same length
        Y1 = Y1[:min_length]
        Y2 = Y2[:min_length]

        M_Y1 = math_exp(Y1)
        M_Y2 = math_exp(Y2)
        sigma_Y1 = sigma(Y1, M_Y1)
        sigma_Y2 = sigma(Y2, M_Y2)

        cur_R = np.sum((Y1 - M_Y1) * (Y2 - M_Y2))  # Calculate correlation

        if K * (quantity_frames - abs(offset)) > 0:
            cur_R /= (K * (quantity_frames - abs(offset)) * sigma_Y1 * sigma_Y2)

        list_R.append(cur_R)
        offset += 1

    return list_R


def math_exp(array):
    """Calculates the mean of the array."""
    return array.sum() / array.size


def sigma(array, mean_exp):
    """Calculates the standard deviation of the array."""
    return sqrt(np.sum((array - mean_exp) ** 2) / array.size)


def RGBtoY_str(array_list):
    """Converts RGB frames to Y channel."""

    K_R = 0.299
    K_B = 0.114
    K_G = 0.587

    Y_list = [K_R * RGB[0] + K_G * RGB[1] + K_B * RGB[2]
              for array in array_list
              for str_ar in array
              for RGB in str_ar]

    return np.array(Y_list, dtype='float')


def calculate_autocorrelation(*video_files: str):
    matplotlib.use('TkAgg')

    for video_file in video_files:
        args = input_video(video_file, 'rgb24')

        # Calculate autocorrelation using the updated function.
        autocorr_values = autocorrelation(RGBtoY_str(args[0]), last_width, last_height, last_numb_frames)

        plt.plot(range(-last_numb_frames + 1, last_numb_frames), autocorr_values,
                 label=f"R for {video_file.split('/')[-1]}")

    plt.ylabel("R")
    plt.xlabel("Offset")
    plt.grid()
    plt.legend()
    plt.show()
