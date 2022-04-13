import glob
from threading import Thread

import time, datetime

from VideoSplitter import VideoSplitter
from VideoStreamer import VideoStreamer
from StreamData import StreamData





class StreamSync(object):
    def __init__(self) -> None:
        self.chunk_dir = '/home/john/Downloads/temp'
        self.file_prefix = 'tmp_file_stream-'

        #self.stream_link_in = 'http://stream.euroasia.lfstrm.tv/perviy_evrasia/1/index.m3u8'
        self.stream_link_in = 'udp://127.0.0.1:1234'

        self.stream_link_out = 'udp://127.0.0.1:2222?pkt_size=1316'

        self.stream_data_list = []

        self.video_splitter = VideoSplitter(self.chunk_dir, self.file_prefix, self.stream_link_in)
        self.video_streamer = VideoStreamer(self.stream_data_list, self.stream_link_out)
     
        self.video_splitter_thread = Thread(target=self.video_splitter.run)
        self.video_streamer_thread = Thread(target=self.video_streamer.run)
    
    
    def start_splitter(self):
        self.video_splitter_thread.start()
        
    def start_streamer(self):
        self.video_streamer_thread.start()

    def get_file_chunks(self):
        if self.chunk_dir[-1] != '/':
            self.chunk_dir += '/'
        return sorted(glob.glob(self.chunk_dir + '*'))
    
    def get_ready_chunk_list(self):
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
        for path in chunks:
            if not search(path):
                if 'tmp_file_stream-2.ts' in path:
                    self.stream_data_list.append(StreamData(path, [(datetime.datetime.strptime('00:00:10', "%H:%M:%S"), '/home/john/Downloads/ads.mp4')]))
                else:
                    self.stream_data_list.append(StreamData(path, []))
    
    
    def run(self):
        self.start_splitter()
        while len(self.get_file_chunks()) < 3:
            print(f'sleep current batchize {len(self.get_file_chunks())}')
            time.sleep(4)

        self.get_ready_chunk_list()
        self.start_streamer()
        while True:
            time.sleep(5)
            self.get_ready_chunk_list()
            print(f'current batchize {len(self.get_file_chunks())}')



if __name__ == '__main__':
    StreamSync().run()

        

