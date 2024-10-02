import numpy as np
import av
from av.video.frame import VideoFrame
from matplotlib import pyplot as plt
from numpy import sqrt

K_R = 0.299
K_B = 0.114
K_G = 0.587
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
        cur_R = 0

        Y1 = Y_array.copy()
        Y2 = Y_array.copy()

        if offset > 0:
            Y1 = Y1[int(K) * offset:]
            Y2 = Y2[:-int(K) * offset]
        elif offset < 0:
            Y1 = Y1[:-int(K) * offset]
            Y2 = Y2[int(K) * offset:]

        len_Y1, len_Y2 = len(Y1), len(Y2)

        if len_Y1 == 0 or len_Y2 == 0:
            print(f"Warning: One of the arrays is empty after offset adjustment for offset {offset}.")
            list_R.append(0)  # Append a default value if arrays are empty
            offset += 1
            continue

        M_Y1 = math_exp(Y1)
        M_Y2 = math_exp(Y2)
        sigma_Y1 = sigma(Y1, M_Y1)
        sigma_Y2 = sigma(Y2, M_Y2)

        # Ensure we do not exceed the lengths of the arrays
        max_length = min(len_Y1, len_Y2)

        for j in range(max_length):
            cur_R += (Y1[j] - M_Y1) * (Y2[j] - M_Y2)

        if K * (quantity_frames - abs(offset)) > 0:
            cur_R /= (K * (quantity_frames - abs(offset)) * sigma_Y1 * sigma_Y2)

        list_R.append(cur_R)
        print(f"Offset {offset} complete")
        offset += 1

    print("Autocorrelation stop working\n")
    return list_R


def math_exp(array):
    """Calculates the mean of the array."""
    return array.sum() / array.size


def sigma(array, mean_exp):
    """Calculates the standard deviation of the array."""
    return sqrt(np.sum((array - mean_exp) ** 2) / array.size)


def RGBtoY_str(array_list):
    """Converts RGB frames to Y channel."""
    Y_list = [K_R * RGB[0] + K_G * RGB[1] + K_B * RGB[2]
              for array in array_list
              for str_ar in array
              for RGB in str_ar]
    return np.array(Y_list, dtype='float')


if __name__ == "__main__":
    video_files = [
        'C:\\Users\\dryag\\Documents\\suai-multimedia\\resources\\lr1_1.AVI',
        'C:\\Users\\dryag\\Documents\\suai-multimedia\\resources\\lr1_2.AVI',
        'C:\\Users\\dryag\\Documents\\suai-multimedia\\resources\\lr1_3.AVI'
    ]

    for video_file in video_files:
        args = input_video(video_file, 'rgb24')
        plt.plot(range(-last_numb_frames + 1, last_numb_frames),
                 autocorrelation(RGBtoY_str(args[0]), last_width, last_height, last_numb_frames),
                 label=f"R for {video_file.split('/')[-1]}")

    plt.ylabel("R")
    plt.xlabel("Offset")
    plt.grid()
    plt.legend()
    plt.show()


