# import the opencv library
import cv2
import imagehash
from PIL import Image, ImageChops

import concurrent.futures
import pyaudio, wave
import cv2


audio_frames = []


class Aud_Vid():

	def __init__(self, arg):
		self.video = cv2.VideoCapture(0)
		self.CHUNK = 1470
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 2
		self.RATE = 44100
		self.audio = pyaudio.PyAudio()
		self.instream = self.audio.open(format=self.FORMAT,channels=self.CHANNELS,rate=self.RATE,input=True,frames_per_buffer=self.CHUNK)
		self.outstream = self.audio.open(format=self.FORMAT,channels=self.CHANNELS,rate=self.RATE,output=True,frames_per_buffer=self.CHUNK)


	def sync(self):
		global audio_frames
		flag = 1
		with concurrent.futures.ThreadPoolExecutor() as executor:
			while (1):
				tv = executor.submit(self.video.read)
				ta = executor.submit(self.instream.read,1470)
				vid = tv.result()
				aud = ta.result()
				audio_frames.append(aud)


				if flag and cv2.waitKey(1) & 0xFF == ord('q'):
					break
			return(vid[1].tobytes(),aud)



A = Aud_Vid(None).sync()


FORMAT = pyaudio.paInt16
waveFile = wave.open('out.wav', 'wb')
waveFile.setnchannels(A.CHANNELS)
waveFile.setsampwidth(A.audio.get_sample_size(FORMAT))
waveFile.setframerate(A.RATE)
waveFile.writeframes(b''.join(audio_frames))
waveFile.close()



def get_frame_hash(frame):
    image = Image.fromarray(frame)
    return imagehash.phash(image)

# define a video capture object
vid = cv2.VideoCapture(0)


previous_frame = frame = vid.read()[1]
while(vid.isOpened()):
	
	# Capture the video frame
	# by frame
	ret, frame = vid.read()

	current_frame = frame

	# Display the resulting frame
	cv2.imshow('frame', frame)
	
	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	print(get_frame_hash(current_frame) - get_frame_hash(previous_frame))
	previous_frame = current_frame

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

