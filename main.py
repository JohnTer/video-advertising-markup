from AudioProccessor import AudioProccessor
from VideoProcessor import VideoProccessor
from MarkupProccessor import MarkupProccessor
from FileProccessor import FileProccessor


if __name__ == '__main__':

    s = '/Users/vadimterentev/Downloads/output.mp4'
    a = VideoProccessor(s)
    a.open_video()
    r = a.get_frame_hashvector_diff()
    q = MarkupProccessor().get_score(r)


    fp = FileProccessor(s, '/Users/vadimterentev/Downloads/ffmpeg')
    audio = fp.get_audio_from_video()
    AP = AudioProccessor(audio)
    AP.read_file_wav()
    silent = AP.get_silent(AP.get_speech()[0])[1]
    

    ll = MarkupProccessor().get_score(silent)
    hh = MarkupProccessor().calculate_ads_score(q, ll)

    g = 9