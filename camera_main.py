# import the opencv library
import cv2
import imagehash
from PIL import Image, ImageChops


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

