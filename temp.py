
x = input()
print(x * int(x))

exit() 




# import required libraries
from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
import cv2

# Open live video stream on webcam at first index(i.e. 0) device
stream = VideoGear(source=0).start()

# change with your webcam soundcard, plus add additional required FFmpeg parameters for your writer
output_params = {
    "-input_framerate": stream.framerate,
    "-thread_queue_size": "512",
    "-ac": "2",
    "-ar": "48000",
    "-f": "alsa", # !!! warning: always keep this line above "-i" parameter !!!
    "-i": "hw:1",
}

# Define writer with defined parameters and suitable output filename for e.g. `Output.mp4
writer = WriteGear(output_filename="Output.mp4", logging=True, **output_params)

# loop over
while True:

    # read frames from stream
    frame = stream.read()

    # check for frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}

    # write frame to writer
    #writer.write(frame)

    # Show output window
    cv2.imshow("Output Frame", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close video stream
stream.stop()

# safely close writer
writer.close()
