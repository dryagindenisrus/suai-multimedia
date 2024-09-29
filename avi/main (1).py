import numpy
import numpy as np
import av
from av.video.frame import VideoFrame
import pip
from matplotlib import pyplot as plt

from numpy import sqrt


def install(package):
    pip.main(['install', package])


class VideoHandler:
    __K_R = 0.299
    __K_B = 0.114
    __K_G = 0.587
    last_height = None
    last_width = None
    last_numb_frames = None

    def __init__(self):
        super().__init__()

    # Возвращает видео в виде списка, содержащего кадры в виде numpy array
    @staticmethod
    def input_video(path, reformat_name=None):
        array_list = []
        input_container = av.open(path)

        format_container_name = input_container.format.name
        codec_name = input_container.streams.video[0].codec_context.name
        frame_width = input_container.streams.video[0].codec_context.width
        frame_height = input_container.streams.video[0].codec_context.height
        rate = input_container.streams.video[0].average_rate
        # print(rate)
        format_frame_name = input_container.streams.video[0].codec_context.format.name

        VideoHandler.last_height = frame_height
        VideoHandler.last_width = frame_width
        VideoHandler.last_numb_frames = input_container.streams.video[0].frames

        if reformat_name is None:
            reformat_name = format_frame_name

        # counter = 0
        for frame in input_container.decode(video=0):
            frame = frame.reformat(frame_width, frame_height, reformat_name)
            array = frame.to_ndarray()
            array_list += [array]
            # counter = counter + 1
        # print(counter)
        input_container.close()
        return array_list, format_container_name, reformat_name, codec_name, rate

    @staticmethod
    # @time_of_work
    def output_video(path, array_list, format_container_name, format_frame_name, codec_name, rate):
        output_container = av.open(path, mode='w')
        output_stream = output_container.add_stream(codec_name, rate=rate)
        output_stream.height = 120
        output_stream.width = 176
        for array in array_list:
            frame = VideoFrame.from_ndarray(array.astype(np.uint8), format=format_frame_name)
            # # frame = frame.reformat(176, 120, format_frame_name)
            # frame2 = frame.reformat(176, 120, 'rgb24')
            frame2 = output_stream.encode(frame)
            output_container.mux(frame2)

        output_container.close()

    @staticmethod
    # @time_of_work
    def output_reverse_video(path, array_list, format_container_name, format_frame_name, codec_name, rate,
                             count_frame_quantity):
        array_list_out = []
        count = 0
        for array in array_list:
            frame = VideoFrame.from_ndarray(array, format=format_frame_name)
            # frame.pts = count_frame_quantity - count
            array_list_out += [frame.to_ndarray()]
            count += 1
        array_list_out.reverse()
        VideoHandler.output_video(path, array_list_out, format_container_name, format_frame_name, codec_name, rate)

    @staticmethod
    # @time_of_work
    def autocorrelation(Y_array, width, height, quantity_frames):
        print(
            f"autocorrelation start working, data:\nwidth: {width}\nheight: {height}\nquantity_frames: {quantity_frames}")
        K = width * height
        offset = - quantity_frames + 1
        Y1 = Y_array[::]
        Y2 = Y_array[::]
        list_R = []
        while offset < quantity_frames:
            j = 0
            cur_R = 0

            Y1 = list(Y_array)
            Y2 = list(Y_array)
            if offset > 0:
                del Y1[0:int(K) * offset]
                del Y2[-int(K) * offset:]
            elif offset == 0:
                pass
            else:
                del Y1[int(K) * offset:]
                del Y2[0:-int(K) * offset]
            Y1 = np.array(Y1)
            Y2 = np.array(Y2)

            M_Y1 = VideoHandler.math_exp(Y1)
            M_Y2 = VideoHandler.math_exp(Y2)
            sigma_Y1 = VideoHandler.sigma(Y1, M_Y1)
            sigma_Y2 = VideoHandler.sigma(Y2, M_Y2)

            while j <= K * (quantity_frames - abs(offset)) - 1:
                cur_R += (Y1[j] - M_Y1) * (Y2[j] - M_Y2)
                j += 1

            cur_R /= (K * (quantity_frames - abs(offset)) * sigma_Y1 * sigma_Y2)
            list_R += [cur_R]

            print(f"Offset {offset} complete")

            offset += 1

        print("autocorrelation stop working\n")
        return list_R

    @staticmethod
    def math_exp(array):
        return array.sum() / array.size

    @staticmethod
    def sigma(array, math_exp):
        res = 0
        for el in array:
            res += pow(el - math_exp, 2)
        return sqrt(res / array.size)

    @classmethod
    # @time_of_work
    def RGBtoY_str(cls, array_list):
        # Y_list = []
        Y_list = [cls.__K_R * RGB[0] + cls.__K_G * RGB[1] + cls.__K_B * RGB[2]
                  for array in array_list
                  for str_ar in array
                  for RGB in str_ar
                  ]

        return np.array(Y_list, dtype='float')


if __name__ == "__main__":
    args = VideoHandler.input_video('resources/lr1_3.avi', 'rgb24')
    plt.plot(range(-VideoHandler.last_numb_frames + 1, VideoHandler.last_numb_frames), VideoHandler.autocorrelation(
        VideoHandler.RGBtoY_str(args[0]), VideoHandler.last_width, VideoHandler.last_height,
        VideoHandler.last_numb_frames), label="R for 3.avi")
    args = VideoHandler.input_video('resources/lr1_2.avi', 'rgb24')
    plt.plot(range(-VideoHandler.last_numb_frames + 1, VideoHandler.last_numb_frames), VideoHandler.autocorrelation(
        VideoHandler.RGBtoY_str(args[0]), VideoHandler.last_width, VideoHandler.last_height,
        VideoHandler.last_numb_frames), label="R for 2.avi")
    args = VideoHandler.input_video('resources/lr1_1.avi', 'rgb24')
    plt.plot(range(-VideoHandler.last_numb_frames + 1, VideoHandler.last_numb_frames), VideoHandler.autocorrelation(
        VideoHandler.RGBtoY_str(args[0]), VideoHandler.last_width, VideoHandler.last_height,
        VideoHandler.last_numb_frames), label="R for 1.avi")
    plt.ylabel("R")
    plt.xlabel("Offset")
    plt.grid()
    plt.legend()
    plt.show()
    args = VideoHandler.input_video('resources/lr1_1.avi', 'rgb24')

    VideoHandler.output_reverse_video('resources/inversion.avi', args[0], args[1], args[2], args[3], args[4],
                                      VideoHandler.last_numb_frames)

    array_list1, format_container_name, format_frame_name, codec_name, rate = VideoHandler.input_video(
        'resources/lr1_1.avi', 'rgb24')
    args = VideoHandler.input_video('resources/lr1_2.avi', 'rgb24')
    array_list2 = args[0]

    VideoHandler.output_video('resources/union.avi', array_list1 + array_list2, format_container_name,
                              format_frame_name, codec_name, rate)
