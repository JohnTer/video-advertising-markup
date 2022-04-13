
from pathlib import Path
import subprocess
from StreamData import StreamData
import datetime


class VideoStreamer(object):
    def __init__(self, batch_list) -> None:

        self.batch_list = batch_list
        self.ffmpeg_path = 'ffmpeg'
        self.stream_link = 'udp://127.0.0.1:2222?pkt_size=1316'

        #self.ffmpeg_command = r'{} -re -fflags nobuffer -flags low_delay  -ss {} -i {} {} -c:v copy  -c:a  aac -f mpegts {}'
        self.ffmpeg_command = r'{} -re -ss {} -i {} {} -c:v copy  -c:a  copy -bsf:v h264_mp4toannexb -fflags nobuffer -f mpegts {}'
        self.run_flag = False

    def get_shell_command(self, input_video_path, start_time, stop_time=None):
        command = self.ffmpeg_command
        if stop_time is None:
            stop_time_str = ''
        else:
            stop_time_str = '-to ' + \
                str((stop_time - start_time).seconds)

        if start_time != datetime.datetime.strptime('00:00:00', "%H:%M:%S"):
            start_time -= datetime.timedelta(seconds=5)
        start_time_str = start_time.strftime("%H:%M:%S")

        command = command.format(
            self.ffmpeg_path, start_time_str, input_video_path, stop_time_str, self.stream_link)

        with open('cmd_stream.sh', 'w') as f:
            f.write(command)
        with open('cmd_add.txt', 'a') as f:
            f.write(command+'\n')
        return command.split()

    def run(self):
        a = StreamData('/home/john/Downloads/out.mp4',
                       [(datetime.datetime.strptime('00:00:30', "%H:%M:%S"), '/home/john/Downloads/ads.mp4'),
                        (datetime.datetime.strptime('00:01:20', "%H:%M:%S"), '/home/john/Downloads/ads2.mp4')])
        chunk_list = [a]

        for chunk in chunk_list:
            file_stream_path = chunk.local_path

            prev_ad_time = datetime.datetime.strptime('00:00:00', "%H:%M:%S")
            for ad in chunk.ads_list:
                ad_start_time = ad[0]
                ad_path = ad[1]

                self.start_stream(file_stream_path,
                                  prev_ad_time, ad_start_time)
                self.start_stream(ad_path)

                prev_ad_time = ad_start_time
            self.start_stream(file_stream_path, prev_ad_time)

    def start_stream(self, file_stream_path, start_time=datetime.datetime.strptime('00:00:00', "%H:%M:%S"), stop_time=None):
        cmd = self.get_shell_command(
            file_stream_path, start_time, stop_time)
        process = subprocess.Popen(['bash', '-x', 'cmd_stream.sh'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)

        while True:
            output = process.stdout.readline()
            print(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                print('RETURN CODE', return_code)
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    print(output.strip())
                break


e = [{'path': '', 'ads': {'00:10': 'path'}}]


if __name__ == '__main__':
    VideoStreamer([]).run()
