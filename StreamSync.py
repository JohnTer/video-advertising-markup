import glob, os, stat
import sys
from threading import Thread

import time, datetime

from VideoSplitter import VideoSplitter
from VideoStreamer import VideoStreamer
from StreamData import StreamData, AdData
import subprocess

from AudioProccessor import AudioProccessor
from VideoProcessor import VideoProccessor
from MarkupProccessor import MarkupProccessor
from FileProccessor import FileProccessor


class StreamSync(object):
    def __init__(self) -> None:

        self.ffmpeg_path = 'ffmpeg'


        self.chunk_dir = '/dev/shm/temp'
        self.file_prefix = 'tmp_file_stream-'

        self.stream_link_in = 'http://stream.euroasia.lfstrm.tv/perviy_evrasia/1/index.m3u8'
        
        
        
        self.stream_link_in = 'http://livetv.mylifeisgood.ml/mfolive.m3u8?media=sts'

        #self.stream_link_in = 'udp://127.0.0.1:1234'

        self.stream_link_out = 'udp://127.0.0.1:2222?pkt_size=1316'

        self.stream_data_list = []

        self.buffer_pipe_path = '/dev/shm/temp/mypipe'
        self.chunk_size = 10
        self.current_buffer_time = 0
        
        if self.chunk_dir[-1] != '/':
            self.chunk_dir += '/'

        self.video_splitter = VideoSplitter(self.chunk_dir, self.file_prefix, self.stream_link_in, self.chunk_size)
        self.video_streamer = VideoStreamer(self.stream_data_list, self.stream_link_out, self.buffer_pipe_path)
     
        self.video_splitter_thread = Thread(target=self.video_splitter.run)
        self.video_streamer_thread = Thread(target=self.video_streamer.run)


        self.ffmpeg_command_f = r'{} -i {} -vcodec copy -acodec copy -t {} {}'
        self.ffmpeg_command_s = r'{} -i {} -vcodec copy -acodec copy -ss {} {}'

        self.ap = AudioProccessor()
        self.video_processor = VideoProccessor()


    def get_shell_command(self, input_file, split_time, output_file_f, output_file_s):
        command = self.ffmpeg_command_f.format(
            self.ffmpeg_path, input_file, split_time.strftime("%H:%M:%S"), output_file_f)

        with open('cmd_split_f.sh', 'w') as f:
            f.write(command)

        command = self.ffmpeg_command_s.format(
            self.ffmpeg_path, input_file, split_time.strftime("%H:%M:%S"), output_file_s)

        with open('cmd_split_s.sh', 'w') as f:
            f.write(command)

    def get_stream_data_with_ads(self, sd):
        filepath = sd.local_path

        vp = VideoProccessor(filepath)
        vp.open_video()
        vp_hashvector_diff = vp.get_frame_hashvector_diff()
        vp_hashvector_score = MarkupProccessor().get_score(vp_hashvector_diff)


        fp = FileProccessor(filepath, self.ffmpeg_path)
        audio = fp.get_audio_from_video()
        
        self.ap.read_file_wav(audio)
        silent_vector = self.ap.get_silent(self.ap.get_speech()[0])[1]
        

        silent_vector_score = MarkupProccessor().get_score(silent_vector)
        
        self.result = MarkupProccessor().calculate_ads_score(vp_hashvector_score, silent_vector_score)
        self.result.sort(key=lambda d: d['weight'], reverse=True)
        
        timecode = self.result[0]

        ads_time = datetime.datetime.fromtimestamp(timecode['time'])
        ads_path = '/home/john/Downloads/ads5.ts'
        sd.add_ads(ads_path, ads_time)
        
        return sd


    
    def create_buffer_pipe(self):
        with open(self.buffer_pipe_path, 'w') as f:
            pass
        
        # if not stat.S_ISFIFO(os.stat(self.buffer_pipe_path).st_mode):
        #     os.mkfifo(self.buffer_pipe_path)
    
    def start_splitter(self):
        self.video_splitter_thread.start()
        
    def start_streamer(self):
        self.video_streamer_thread.start()

    def get_file_chunks(self):

        files = [f for f in glob.glob(self.chunk_dir + '*') if self.file_prefix in f]
        return sorted(files, key=lambda name: int(name.split('-')[-1].split('.')[0]))
    
    
    def split_video(self, path, split_time):
        ftmp_file = self.chunk_dir + 'temp1.ts'
        stmp_file = self.chunk_dir + 'temp2.ts'


        self.get_shell_command(path, split_time, ftmp_file, stmp_file)
        process = subprocess.Popen(['bash', '-x', 'cmd_split_f.sh'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL,
                                   universal_newlines=True)

        process = subprocess.Popen(['bash', '-x', 'cmd_split_s.sh'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL,
                                   universal_newlines=True)
        return ftmp_file, stmp_file
    
    
    def ads_preproccessor(self, stream_data):
        if self.current_buffer_time % 60 != 0 or self.current_buffer_time == 0:
            return stream_data


        stream_data = self.get_stream_data_with_ads(stream_data)

        split_files = self.split_video(stream_data.local_path, datetime.datetime.strptime('00:00:10', "%H:%M:%S"))
        stream_data.binary_data_parts.clear()
    
        for filename in split_files:
            while not os.path.exists(filename):
                time.sleep(1)
            with open(filename, 'rb') as f:
                data = f.read()
                stream_data.binary_data_parts.append(data)
            os.unlink(filename)
        
        stream_data.ads_proccessed = True
            
        return stream_data
    
    
    
    def prepare_chunk_list(self):
        #a = StreamData('/home/john/Downloads/out.mp4',
        #               [(datetime.datetime.strptime('00:00:30', "%H:%M:%S"), '/home/john/Downloads/ads.mp4'),
        #                (datetime.datetime.strptime('00:01:20', "%H:%M:%S"), '/home/john/Downloads/ads2.mp4')])
        #chunk_list = [a]

        def search(path):
            for obj in self.stream_data_list:
                if obj.local_path == path:
                    return True
            return False
        
        
        chunks = self.get_file_chunks()
        del chunks[-1]
        for path in chunks:
            self.current_buffer_time += self.chunk_size

            data = b''
            while len(data) == 0:
                with open(path, 'rb') as f:
                    data = f.read()
            sd = StreamData(path)
            sd.binary_data_parts.append(data)
            sd.loaded = True
            
            sd = self.ads_preproccessor(sd)
            os.unlink(path)
            self.stream_data_list.append(sd)

        
    
    
    def run(self):
        self.create_buffer_pipe()
        self.start_splitter()
        while len(self.get_file_chunks()) < 5:
            time.sleep(4)

        self.prepare_chunk_list()
        self.start_streamer()
        while True:
            time.sleep(2)
            self.prepare_chunk_list()



if __name__ == '__main__':
    #t = datetime.datetime.strptime('00:00:10', "%H:%M:%S")
    #p = '/home/john/Downloads/ads.mp4'
    #StreamSync().split_video(p, t)
    StreamSync().run()

        

