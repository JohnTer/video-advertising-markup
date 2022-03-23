from tkinter.messagebox import NO
from typing import Callable
import torch
import wave


class AudioProccessor(object):

    TORCH_REPO_NAME: str = 'snakers4/silero-vad'
    TORCH_MODEL_NAME: str = 'silero_vad'

    def __init__(self, wav_filename: str) -> None:
        self.filename = wav_filename

        self.model = None
        self.get_speech_timestamps = None
        self.duration = None

        self._init_torch_model()
        self._init_framerate()

    def _init_torch_model(self):
        model, utils = torch.hub.load(repo_or_dir=AudioProccessor.TORCH_REPO_NAME,
                                      model=AudioProccessor.TORCH_MODEL_NAME)

        self.functions = {}

        self.functions['get_speech_timestamps'] = utils[0]
        self.functions['read_audio'] = utils[2]
        self.model = model

    def _init_framerate(self) -> float:
        with wave.open(self.filename) as bwav:
            frames = bwav.getnframes()
            self.sample_rate = bwav.getframerate()
            self.duration = frames / float(self.sample_rate)

        return self.sample_rate

    def read_file_wav(self):
        self.wav: Callable = self.functions['read_audio'](self.filename)

    def get_speech(self, seconds_flag: bool = True):
        def weight_function(v):
            return v[1] - v[0]
        
        speech_timestamps = self.functions['get_speech_timestamps'](
            self.wav, self.model, return_seconds=seconds_flag)
        noise_vector = [(x['start'], x['end']) for x in speech_timestamps]

        noise_vector_with_weight = []
        for v in noise_vector:
            noise_vector_with_weight.append(
                {'time': v, 'weight': weight_function(v)})

        return noise_vector, noise_vector_with_weight

    def get_silent(self, noise_vector: list):
        def weight_function(v):
            return v[1] - v[0]
        silent_vector: list = []

        silent_vector.append((0, noise_vector[0][0]))
        for i in range(len(noise_vector)-1):
            silent_vector.append((noise_vector[i][1], noise_vector[i+1][0]))
        else:
            silent_vector.append(
                (noise_vector[-1][1], round(self.duration, 1)))

        silent_vector_with_weight = []
        for v in silent_vector:
            silent_vector_with_weight.append(
                {'time': v, 'weight': weight_function(v)})

        return silent_vector, silent_vector_with_weight



if __name__ == '__main__':
    A = AudioProccessor('../OSR_us_000_0010_8k.wav')
    A.read_file_wav()
    h = A.get_silent(A.get_speech()[0])

    f = 9
