from operator import sub
import os
import subprocess



class FileProccessor(object):

    TMP_PATH = '/tmp'

    def __init__(self) -> None:
        self._video_path = '/Users/vadimterentev/Downloads/BigBuckBunny.mp4'
        self._ffmpeg_path = '/Users/vadimterentev/Downloads/ffmpeg'
        self._ffmpeg_param = '-i {} -vn -acodec pcm_s16le -ar 44100 -ac 1 {}'

        self._sound_dir = FileProccessor.TMP_PATH


    def get_audio_from_video(self, video_path: str):
        filename = os.path.basename(video_path) + '.wav'

        output_path = os.path.join(self._sound_dir, filename)
        cmd_params: str = self._ffmpeg_param.format(video_path, output_path).split()
        cmd = [self._ffmpeg_path]
        cmd.extend(cmd_params)
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        return output_path


if __name__ == '__main__':
    A = FileProccessor()
    s = '/Users/vadimterentev/Downloads/BigBuckBunny.mp4'
    v = A.get_audio_from_video(s)
    f = 9