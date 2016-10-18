from imutils.video import FPS
from imutils.video import WebcamVideoStream
import cv2
import argparse
import imutils
import datetime
import time

print("[INFO] sampling frames from webcam...")
#stream = cv2.VideoCapture(0)
vs = WebcamVideoStream(src=0).start()
time.sleep(2.0)

while True:
    #(grabbed, frame) = stream.read()
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

#stream.release()
cv2.destroyAllWindows()
vs.stop()
