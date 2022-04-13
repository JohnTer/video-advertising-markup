
from pathlib import Path
import subprocess



class VideoStreamer(object):
    def __init__(self, batch_list) -> None:

        self.batch_list = batch_list
        self.ffmpeg_path = '/Users/vadimterentev/Downloads/ffmpeg'
        self.stream_link = 'udp://127.0.0.1:2222?pkt_size=1316'
        self.skip_sec = 0
        
        self.ffmpeg_command = r'{}  -re -ss {} -i {} -c:v copy  -c:a  aac -f mpegts {}'
        self.run_flag = False

    def get_shell_command(self, input_video_path):
        command = self.ffmpeg_command
        command = command.format(self.ffmpeg_path, self.skip_sec, input_video_path ,self.stream_link)
        with open('cmd_stream.sh', 'w') as f:
            f.write(command)
        return command.split()

    def run(self):
        self.run_service()
    
    def run_service(self):
        cmd = self.get_shell_command('/tmp/batch/tmp_file_stream-0.ts')
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
        


