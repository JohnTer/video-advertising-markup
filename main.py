from AudioProccessor import AudioProccessor
from VideoProcessor import VideoProccessor
from MarkupProccessor import MarkupProccessor
from FileProccessor import FileProccessor

import numpy as np
import ckwrap, cv2

class AdsMarkup(object):
    def __init__(self, filepath, ffmpeg_path = 'ffmpeg') -> None:
        self.filepath = filepath
        self.ffmpeg_path = ffmpeg_path
        self.result = None

    def get_markup_vector(self):
        vp = VideoProccessor(self.filepath)
        vp.open_video()
        vp_hashvector_diff = vp.get_frame_hashvector_diff()
        vp_hashvector_score = MarkupProccessor().get_score(vp_hashvector_diff)


        fp = FileProccessor(self.filepath, self.ffmpeg_path)
        audio = fp.get_audio_from_video()
        ap = AudioProccessor()
        ap.read_file_wav(audio)
        silent_vector = ap.get_silent(ap.get_speech()[0])[1]
        

        silent_vector_score = MarkupProccessor().get_score(silent_vector)
        
        self.result = MarkupProccessor().calculate_ads_score(vp_hashvector_score, silent_vector_score)
        self.result.sort(key=lambda d: d['weight'], reverse=True)

        return self.result, vp_hashvector_diff

    def get_top_result(self, top=5):
        return self.result[:top]


if __name__ == '__main__':

    s = '/home/john/Downloads/videos/лайфхак/out.mp4'
    f = 'ffmpeg'

    a = AdsMarkup(s, f)
    _, c = a.get_markup_vector()
    v = a.get_top_result()


    К = 5
    nums= np.array([x['time'] for x in  a.result])
    km = ckwrap.ckmeans(nums, К)

    print(km.labels)
    # [0 0 0 0 1 1 1 2 2]


    buckets = [[] for _ in  range(К)]
    for i in range(len(nums)):



        buckets[km.labels[i]].append(a.result[i])
    

    for ind, t in enumerate(buckets):
        mx = max(t, key=lambda x: x['weight'])
        i = t.index(mx)

        new_time = round(mx['time'])
        print(new_time, mx['weight'])

        
        cv2.imwrite(f'results/{ind}_pre_{new_time}.jpg', mx['raw0'])
        cv2.imwrite(f'results/{ind}_cur_{new_time}.jpg', mx['raw1'])
        


    g = 9