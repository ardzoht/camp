/*global $, WebSocket, console, window, document*/
"use strict";

var baseURL = "http://10.33.8.140:8000/GPIO/";
var username = "webiopi";
var password = "raspberry";

/**
 * Connects to Pi server and receives video data.
 */
var client = {

    // Connects to Pi via websocket
    connect: function (port) {
        var self = this, video = document.getElementById("video");

        this.socket = new WebSocket("ws://" + "10.33.8.140" + ":" + port + "/websocket");
	
	console.log("Connecting to: " + this.socket.url);

        // Request the video stream once connected
        this.socket.onopen = function () {
            console.log("Connected!");
            self.readCamera();
        };

        // Currently, all returned messages are video data. However, this is
        // extensible with full-spec JSON-RPC.
        this.socket.onmessage = function (messageEvent) {
            console.log(messageEvent);
            video.src = "data:image/jpeg;base64," + messageEvent.data;
        };
    },

    // Requests video stream
    readCamera: function () {
        this.socket.send("read_camera");
    }
};
