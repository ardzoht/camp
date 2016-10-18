import datetime
from threading import Thread
import cv2

class FPS:
    def __init__(self):
        self.start = None
        self.end = None
        self.numFrames = 0

    def start(self):
        self.start = datetime.datetime.now()
        return self

    def stop(self):
        self.end = datetime.datetime.now()

    def update(self):
        self.numFrames += 1

    def elapsed(self):
        return (self.end - self.start).total_seconds()

    def get_fps(self):
        return self.numFrames / self.elapsed()

class WebCamVideoStream:
    def __init__(self, src=0):
       #init opencv stream
       self.stream = cv2.VideoCapture(src)
       (self.grabbed, self.frame) = self.stream.read()

       #flag to indicate if thread should be stopped
       self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
        (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
