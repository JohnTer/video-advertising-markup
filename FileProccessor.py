
import os
import subprocess
import typing
import requests



class FileProccessor(object):

    TMP_PATH = '/tmp'

    def __init__(self) -> None:
        self._video_path = '/Users/vadimterentev/Downloads/BigBuckBunny.mp4'
        self._ffmpeg_path = '/Users/vadimterentev/Downloads/ffmpeg'
        self._ffmpeg_param = '-y -i {} -vn -acodec pcm_s16le -ar 44100 -ac 1 {}'

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

    def get_video_from_url(self, url):
        res = requests.get(url, allow_redirects=True)
        with open(self._video_path, 'wb') as fb:
            fb.write(res.content)

if __name__ == '__main__':
    A = FileProccessor()
    s = '/Users/vadimterentev/Downloads/BigBuckBunny.mp4'
    v = A.get_audio_from_video(s)
    url = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
    #A.get_video_from_url(url)