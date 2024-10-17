from avi import reverse_video, combine_videos, union_2_videos_in_frame
from avi import calculate_autocorrelation
from settings import RESOURCES_DIR
from os import path


def main():
    reverse_video(
        path.join(RESOURCES_DIR, 'lr1_1.avi'),
        path.join(RESOURCES_DIR, 'lr1_1_invert.avi')
    )

    combine_videos(
        [
            path.join(RESOURCES_DIR, 'lr1_1.avi'),
            path.join(RESOURCES_DIR, 'lr1_2.avi'),
            path.join(RESOURCES_DIR, 'lr1_3.avi')
        ],
        path.join(RESOURCES_DIR, 'lr1_123_combined.avi')
    )

    union_2_videos_in_frame(
        path.join(RESOURCES_DIR, 'lr1_1.avi'),
        path.join(RESOURCES_DIR, 'lr1_2.avi'),
        path.join(RESOURCES_DIR, 'lr1_123_cut.avi')
    )

    calculate_autocorrelation(
        path.join(RESOURCES_DIR, 'lr1_1.avi'),
        path.join(RESOURCES_DIR, 'lr1_2.avi'),
        path.join(RESOURCES_DIR, 'lr1_3.avi'))


if __name__ == '__main__':
    main()
