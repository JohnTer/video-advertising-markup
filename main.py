from AudioProccessor import AudioProccessor
from VideoProcessor import VideoProccessor
from MarkupProccessor import MarkupProccessor
from FileProccessor import FileProccessor


class AdsMarkup(object):
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.ffmpeg_path = 'ffmpeg'

    def get_markup_vector(self):
        vp = VideoProccessor(s)
        vp.open_video()
        vp_hashvector_diff = vp.get_frame_hashvector_diff()
        vp_hashvector_score = MarkupProccessor().get_score(vp_hashvector_diff)


        fp = FileProccessor(s, 'ffmpeg')
        audio = fp.get_audio_from_video()
        AP = AudioProccessor(audio)
        AP.read_file_wav()
        silent = AP.get_silent(AP.get_speech()[0])[1]
        

        ll = MarkupProccessor().get_score(silent)
        hh = MarkupProccessor().calculate_ads_score(q, ll)
        hh.sort(key=lambda tup: tup['weight'], reverse=True)

    
    


if __name__ == '__main__':

    s = '/home/john/Downloads/timati.mp4'
    a = VideoProccessor(s)
    a.open_video()
    r = a.get_frame_hashvector_diff()
    q = MarkupProccessor().get_score(r)


    fp = FileProccessor(s, 'ffmpeg')
    audio = fp.get_audio_from_video()
    AP = AudioProccessor(audio)
    AP.read_file_wav()
    silent = AP.get_silent(AP.get_speech()[0])[1]
    

    ll = MarkupProccessor().get_score(silent)
    hh = MarkupProccessor().calculate_ads_score(q, ll)
    hh.sort(key=lambda tup: tup['weight'], reverse=True)


    g = 9