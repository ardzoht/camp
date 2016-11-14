#!/usr/bin/env python
"""
Creates an HTTP server with websocket communication.
"""
import argparse
import base64
import hashlib
import os
import time
import threading
import webbrowser

try:
    import cStringIO as io
except ImportError:
    import io

import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback

# Hashed password for comparison and a cookie for login cache
ROOT = os.path.normpath(os.path.dirname(__file__))
with open(os.path.join(ROOT, "password.txt")) as in_file:
    PASSWORD = in_file.read().strip()
COOKIE_NAME = "camp"


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        if args.require_login and not self.get_secure_cookie(COOKIE_NAME):
            self.redirect("/login")
        else:
            self.render("index.html", port=args.port)

class WebSocket(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        """Evaluates the function pointed to by json-rpc."""

        # Start an infinite loop when this is called
        if message == "read_camera":
            self.worker = CaptureThread()
            self.worker.start()
            self.camera_loop = PeriodicCallback(self.loop, 5)
            self.camera_loop.start()

        elif message == "get_frame":
            pass
            #send frame encoded

        else:
            print("Unsupported function: " + message)

    def loop(self):
        """Sends camera images in an infinite loop."""
        frame = self.worker.read_camera()
        _ ,frame = camera.retrieve(frame)
        sio = io.StringIO()
        #_, frame = camera.read()
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img.save(sio, "JPEG")
        #_, image = cv2.imencode('.jpg', frame)
        #numpy.save(sio, image)
        #print image
        try:
            #print("sending message")
            self.write_message(base64.b64encode(sio.getvalue()))
        except tornado.websocket.WebSocketClosedError:
            self.camera_loop.stop()
            print ("Websocket closed (read_camera)")

class CaptureThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "Capture worker started..."

    def read_camera(self):
        frame = camera.grab()
        return frame

    def get_frame(self):
        _ , frame = camera.read()
        sio = io.StringIO()
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img.save(sio, "JPEG")
        try:
            self.write_message(base64.b64encode(sio.getvalue()))
        except tornado.websocket.WebSocketClosedError:
            print ("Websocket closed (get_frame)")

parser = argparse.ArgumentParser(description="Starts a webserver that "
                                 "connects to a webcam.")
parser.add_argument("--port", type=int, default=8000, help="The "
                    "port on which to serve the website.")
parser.add_argument("--resolution", type=str, default="low", help="The "
                    "video resolution. Can be high, medium, or low.")
parser.add_argument("--lights", action="store_true", help= "Use lights controller.")

args = parser.parse_args()

import cv2
from PIL import Image, ImageDraw, ImageFont
camera = cv2.VideoCapture(-1)

resolutions = {"high": (1280, 720), "medium": (640, 480), "low": (320, 240)}
if args.resolution in resolutions:
    w, h = resolutions[args.resolution]
    camera.set(3, w)
    camera.set(4,h)
    time.sleep(2)
    print "Resolution set to: "
    print camera.get(3), camera.get(4)

else:
    raise Exception("%s not in resolution options." % args.resolution)

handlers = [(r"/", IndexHandler),
            (r"/websocket", WebSocket),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': ROOT})]
application = tornado.web.Application(handlers, cookie_secret=PASSWORD)
application.listen(args.port, address="0.0.0.0")

tornado.ioloop.IOLoop.instance().start()
