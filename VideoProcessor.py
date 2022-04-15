
import math
 

import cv2
import time, sys
import imagehash

from PIL import Image, ImageChops

from MarkupProccessor import MarkupProccessor
  
# assign images
#img1 = Image.open("1img.jpg")
#img2 = Image.open("2img.jpg")
#  
## finding difference
#diff = ImageChops.difference(img1, img2)
#  
## showing the difference
#diff.show()




class VideoProccessor(object):
    def __init__(self, filename) -> None:
        self.filename = filename
        self.video_capture = None

        self.fps = None


    def open_video(self):
        self.video_capture = cv2.VideoCapture(self.filename)
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)

    def get_frame_hash(self, frame):
        image = Image.fromarray(frame)
        return imagehash.phash(image)

    def get_frame_hashvector(self):
        success = True
        frame_hash_buffer = []

        while success:
            success, frame = self.video_capture.read()
            frame_hash_buffer.append(self.get_frame_hash(frame))
        return frame_hash_buffer

    def get_frame_hashvector_diff(self):
        success = True
        frame_hash_buffer_diff = []

        success, prev_frame = self.video_capture.read()
        prev_frame_hash = self.get_frame_hash(prev_frame)
        current_frame = None

        frame_count = 0
        while success:
            success, current_frame = self.video_capture.read()
            if not success:
                break

            current_frame_hash = self.get_frame_hash(current_frame)
            frame_time = self.get_frame_time(frame_count)
            data = {
                'time': frame_time,
                'weight': current_frame_hash - prev_frame_hash
            }
            frame_hash_buffer_diff.append(data)
            prev_frame_hash = current_frame_hash # Optimize it! store hash instead of frame

            frame_count += 1
        return frame_hash_buffer_diff

    def get_frame_time(self, frame_count):
        return frame_count / self.fps




    


if __name__ == '__main__':
    s = '/Users/vadimterentev/Downloads/output.mp4'
    a = VideoProccessor(s)
    a.open_video()
    v = a.get_frame_hashvector_diff()
    q = MarkupProccessor().get_speech(v)

    h = 0

    
    








