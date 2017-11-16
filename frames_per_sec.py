from imutils.video import FPS
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
	help="/sample.mp4")
args = vars(ap.parse_args())

stream = cv2.VideoCapture(args["video"])
fps = FPS().start()

while True:
	(grabbed, frame) = stream.read()
 
	if not grabbed:
		break
	frame = imutils.resize(frame, width=450)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame = np.dstack([frame, frame, frame])
 	
 
	# show the frame and update the FPS counter
	cv2.imshow("Frame", frame)
	cv2.waitKey(1)
	fps.update()

fps.stop()
print("elasped time: {:.2f}".format(fps.elapsed()))
print("approx. FPS: {:.2f}".format(fps.fps()))
 

stream.release()
cv2.destroyAllWindows()