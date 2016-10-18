#!/usr/bin/env python
"""
Creates an HTTP server with basic auth and websocket communication.
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

"""
class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        password = self.get_argument("password", "")
        if hashlib.sha512(password).hexdigest() == PASSWORD:
            self.set_secure_cookie(COOKIE_NAME, str(time.time()))
            self.redirect("/")
        else:
            time.sleep(1)
            self.redirect(u"/login?error")

class LightsHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
	   self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
	   self.render("lights.html")
"""

class WebSocket(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        """Evaluates the function pointed to by json-rpc."""

        # Start an infinite loop when this is called
        if message == "read_camera":
            self.worker = CaptureThread()
            self.worker.start()
            self.camera_loop = PeriodicCallback(self.loop, 5)
            self.camera_loop.start()

        # Extensibility for other methods
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
            print ("Websocket closed")

class CaptureThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "Capture worker started..."

    def read_camera(self):
        #e1 = cv2.getTickCount()
        frame = camera.grab()
        #e2 = cv2.getTickCount()
        #time = (e2 - e1) / cv2.getTickFrequency()
        #print time
        return frame

parser = argparse.ArgumentParser(description="Starts a webserver that "
                                 "connects to a webcam.")
parser.add_argument("--port", type=int, default=8000, help="The "
                    "port on which to serve the website.")
parser.add_argument("--resolution", type=str, default="low", help="The "
                    "video resolution. Can be high, medium, or low.")
parser.add_argument("--require-login", action="store_true", help="Require "
                    "a password to log in to webserver.")
parser.add_argument("--lights", action="store_true", help= "Use lights controller.")

args = parser.parse_args()

import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy
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
           #(r"/login", LoginHandler),
           #(r"/lights", LightsHandler),
            (r"/websocket", WebSocket),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': ROOT})]
application = tornado.web.Application(handlers, cookie_secret=PASSWORD)
application.listen(args.port, address="0.0.0.0")

tornado.ioloop.IOLoop.instance().start()
