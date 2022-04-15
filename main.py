from tkinter.messagebox import NO
from AudioProccessor import AudioProccessor
from VideoProcessor import VideoProccessor
from MarkupProccessor import MarkupProccessor
from FileProccessor import FileProccessor


class AdsMarkup(object):
    def __init__(self, filepath, ffmpeg_path = 'ffmpeg') -> None:
        self.filepath = filepath
        self.ffmpeg_path = ffmpeg_path
        self.result = None

    def get_markup_vector(self):
        vp = VideoProccessor(s)
        vp.open_video()
        vp_hashvector_diff = vp.get_frame_hashvector_diff()
        vp_hashvector_score = MarkupProccessor().get_score(vp_hashvector_diff)


        fp = FileProccessor(s, self.ffmpeg_path)
        audio = fp.get_audio_from_video()
        ap = AudioProccessor(audio)
        ap.read_file_wav()
        silent_vector = ap.get_silent(ap.get_speech()[0])[1]
        

        silent_vector_score = MarkupProccessor().get_score(silent_vector)
        
        self.result = MarkupProccessor().calculate_ads_score(vp_hashvector_score, silent_vector_score)
        self.result.sort(key=lambda d: d['weight'], reverse=True)

        return self.result

    def get_top_result(self, top=5):
        return self.result[:top]


if __name__ == '__main__':

    s = '/Users/vadimterentev/Downloads/output.mp4'
    f = '/Users/vadimterentev/Downloads/ffmpeg'

    a = AdsMarkup(s, f)
    a.get_markup_vector()
    v = a.get_top_result()


    g = 9