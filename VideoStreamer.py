
import sys
import time
from pathlib import Path
import subprocess
from StreamData import StreamData
import datetime
from threading import Thread

class VideoStreamer(object):
    def __init__(self, batch_list, stream_link, fifo_buffer) -> None:

        self.batch_list = batch_list
        self.ffmpeg_path = 'ffmpeg'
        self.stream_link = stream_link

        #self.ffmpeg_command = r'{} -re -fflags nobuffer -flags low_delay  -ss {} -i {} {} -c:v copy  -c:a  aac -f mpegts {}'
        self.ffmpeg_command = r'{} -re -stream_loop -1  -i {} -c:v copy  -c:a  copy -bsf:v h264_mp4toannexb -fflags nobuffer -f mpegts {}'
        self.run_flag = False

        self.fifo_buffer = fifo_buffer
        #self.fifo_buffer_file = open(fifo_buffer, 'wb')

    def get_shell_command(self):
        command = self.ffmpeg_command.format(
            self.ffmpeg_path, self.fifo_buffer, self.stream_link)

        with open('cmd_stream.sh', 'w') as f:
            f.write(command)
        return command.split()

    def write_to_buffer(self, data):
        with open(self.fifo_buffer, 'ab') as f:
            f.write(data)
            f.flush()
       
    def run(self):
        #a = StreamData('/home/john/Downloads/temp/tmp_file_stream-0.ts',[])
        #b = StreamData('/home/john/Downloads/temp/tmp_file_stream-1.ts',[])
#
        #a.loaded = True
        #b.loaded = True
#
        #with open(a.local_path, 'rb') as f:
        #    a.binary_data_parts.append(f.read())
#
        #with open(b.local_path, 'rb') as f:
        #    b.binary_data_parts.append(f.read())
#
        #chunk_list = [a, b]

        #self.batch_list  = chunk_list

        Thread(target=self.start_stream).start()
        while True:
            while len(self.batch_list) == 0:
                time.sleep(2)

            chunk = self.batch_list[0]
            while not chunk.loaded:
                time.sleep(2)
                chunk = self.batch_list[0]
            
            for i, ad in enumerate(chunk.ads_list):
                self.write_to_buffer(ad.data)
                self.write_to_buffer(chunk.binary_data_parts[i])

            self.write_to_buffer(chunk.binary_data_parts[-1])
            self.batch_list.pop(0)

            print('stream', len(self.batch_list))
            sys.stdout.flush()

    
    
    def start_stream(self):
        cmd = self.get_shell_command()
        process = subprocess.Popen(['bash', '-x', 'cmd_stream.sh'],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL,
                                   universal_newlines=True)

        while True:
           # output = process.stdout.readline()
            #print(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
              #  print('RETURN CODE', return_code)
                # Process has finished, read rest of the output
                #for output in process.stdout.readlines():
                #    pass
                   # print(output.strip())
                break


e = [{'path': '', 'ads': {'00:10': 'path'}}]


if __name__ == '__main__':

    d = [StreamData(local_path='/home/john/Downloads/temp/tmp_file_stream-0.ts', ads_list=[]), StreamData(local_path='/home/john/Downloads/temp/tmp_file_stream-1.ts', ads_list=[]), StreamData(local_path='/home/john/Downloads/temp/tmp_file_stream-2.ts', ads_list=[(datetime.datetime(1900, 1, 1, 0, 0, 10), '/home/john/Downloads/ads.mp4')]), StreamData(local_path='/home/john/Downloads/temp/tmp_file_stream-3.ts', ads_list=[]), StreamData(local_path='/home/john/Downloads/temp/tmp_file_stream-4.ts', ads_list=[]), StreamData(local_path='/home/john/Downloads/temp/tmp_file_stream-5.ts', ads_list=[]), StreamData(local_path='/home/john/Downloads/temp/tmp_file_stream-6.ts', ads_list=[]), StreamData(local_path='/home/john/Downloads/temp/tmp_file_stream-7.ts', ads_list=[])]
    VideoStreamer(d, 'udp://127.0.0.1:2222?pkt_size=1316', '/home/john/Downloads/temp/mypipe').run()
