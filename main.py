from VideoProcessor import VideoProccessor
from MarkupProccessor import MarkupProccessor


if __name__ == '__main__':

    s = '/Users/vadimterentev/Downloads/output.mp4'
    a = VideoProccessor(s)
    a.open_video()
    r = a.get_frame_hashvector_diff()
    q = MarkupProccessor().get_speech(r)

    g = 9