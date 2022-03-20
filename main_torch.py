import torch
torch.set_num_threads(1)

SAMPLING_RATE = 8000

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True)

(get_speech_ts,
 _, read_audio,
 _, _) = utils

files_dir = torch.hub.get_dir() + '/snakers4_silero-vad_master/files'

wav = read_audio('../OSR_us_000_0010_8k.wav', )
speech_timestamps = get_speech_ts(wav, model, return_seconds=True)
for x in speech_timestamps:
    print(x)