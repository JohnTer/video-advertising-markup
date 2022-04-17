
from pathlib import Path
import subprocess



class VideoSplitter(object):
    def __init__(self, temp_stream_dir, file_prefix, stream_link, chunk_size) -> None:
        self.target_dir = temp_stream_dir
        self.file_prefix = file_prefix
        self.ffmpeg_path = 'ffmpeg'
        self.stream_link = stream_link
        self.chunk_size = chunk_size

        self.ffmpeg_command = r'{} -i {}  -map 0:0 -map 0:1 -s 640x360 -vcodec libx264 -g 60 -vb 500000 -strict experimental -vf yadif -acodec aac -ab 96000 -ac 2 -y -f segment -segment_time {} "{}%01d.ts"'
        self.run_flag = False
    
    
    def create_folder(self):
        path = Path(self.target_dir)
        if not path.is_dir():
            path.mkdir(parents=True)

    def get_shell_command(self):
        command = self.ffmpeg_command
        outpath = self.target_dir + '/' + self.file_prefix if self.target_dir[-1] != '/' else self.target_dir + self.file_prefix 
        command = command.format(self.ffmpeg_path, self.stream_link, self.chunk_size, outpath)
        with open('cmd_split.sh', 'w') as f:
            f.write(command)
        return command.split()

    def run(self):
        self.create_folder()
        self.run_service()
    
    def run_service(self):
        cmd = self.get_shell_command()
        process = subprocess.Popen(['bash', '-x', 'cmd_split.sh'], 
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           universal_newlines=True)
        
        while True:
           # output = process.stdout.readline()
           # print(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
               # print('RETURN CODE', return_code)
                # Process has finished, read rest of the output 
                #for output in process.stdout.readlines():
                #    pass
                  #  print(output.strip())
                break


    


if __name__ == '__main__':
    VideoSplitter().run()
        


