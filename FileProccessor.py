
import os
import subprocess
import typing
import requests
from urllib.parse import urlparse

class FileProccessor(object):

    TMP_PATH: str = '/tmp'
    FFMPEG_PARAM: str = '-y -i {} -vn -acodec pcm_s16le -ar 44100 -ac 1 {}' 

    def __init__(self, file_http_path: str, ffmpeg_path: str) -> None:
        if 'http' in file_http_path:
            self._url = file_http_path
            self._video_path = None
        else:
            self._url = None
            self._video_path = file_http_path


        self._ffmpeg_path = ffmpeg_path

        self._ffmpeg_param = FileProccessor.FFMPEG_PARAM
        self._sound_dir = FileProccessor.TMP_PATH


    def get_audio_from_video(self, video_path: typing.Optional[str] = None):
        video_path = video_path or self._video_path

        filename = os.path.basename(video_path) + '.wav'

        output_path = os.path.join(self._sound_dir, filename)
        cmd_params: str = self._ffmpeg_param.format(video_path, output_path).split()
        cmd = [self._ffmpeg_path]
        cmd += cmd_params
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        assert result.returncode == 0
        
        return output_path

    def get_video_from_url(self, url=None):
        url = url or self._url
        res = requests.get(url, allow_redirects=True)

        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        self._video_path = os.path.join(FileProccessor.TMP_PATH, filename)

        with open(self._video_path, 'wb') as fb:
            fb.write(res.content)

    def run(self, name):
        # self.get_video_from_url()
        self.get_audio_from_video()
        

if __name__ == '__main__':

    fname = '/Users/vadimterentev/Downloads/BigBuckBunny.mp4'
    ffmpeg = '/Users/vadimterentev/Downloads/ffmpeg'


    
    s = '/Users/vadimterentev/Downloads/BigBuckBunny.mp4'
    # v = A.get_audio_from_video(s)
    url = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
    #A.get_video_from_url(url)
    A = FileProccessor('/tmp/BigBuckBunny.mp4', ffmpeg)
    A.run(url)