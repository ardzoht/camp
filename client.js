/*global $, WebSocket, console, window, document*/
"use strict";

var baseURL = "http://10.33.10.18:8000/GPIO/";
var username = "webiopi";
var password = "raspberry";
var gpiofront = 0;
var gpioback = 0;
var gpioleft = 0;
var gpioright = 0;

/**
 * Connects to Pi server and receives video data.
 */
var client = {

    // Connects to Pi via websocket
    connect: function (port) {
        var self = this, video = document.getElementById("video");

        this.socket = new WebSocket("ws://" + window.location.hostname + ":" + port + "/websocket");

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

var handlers = {

    postGPIOHandlerFront: function() {
       if(gpiofront == 0) gpiofront = 1
       else gpiofront = 0

       let completeUrl = baseURL + "2" + "/value/" + gpiofront;
       console.log("posting: " + completeUrl);
        $.ajax({
            url: completeUrl,
            type: 'POST',
            success: function(response) {
                console.log(response);
            }
        });
    },


    postGPIOHandlerBack: function() {
       if(gpioback == 0) gpioback = 1
       else gpioback = 0
       let completeUrl = baseURL + "3" + "/value/" + gpioback;
	
	console.log("posting: " + gpioback);
        $.ajax({
            url: completeUrl,
            type: 'POST',
            success: function(response) {
                console.log(response);
            }
        });
    },


    postGPIOHandlerLeft: function() {
       if(gpioleft == 0) gpioleft = 1
       else gpioleft = 0
       let completeUrl = baseURL + "27" + "/value/" + gpioleft;
	
	console.log("posting: " + gpioleft);	
        $.ajax({
            url: completeUrl,
            type: 'POST',
            success: function(response) {
                console.log(response);
            }
        });
    },

    postGPIOHandlerRight: function() {
       if(gpioright == 0) gpioright = 1
       else gpioright = 0

       let completeUrl = baseURL + "17" + "/value/" + gpioright;

	console.log("posting: " + gpioright);

        $.ajax({
            url: completeUrl,
            type: 'POST',
            success: function(response) {
                console.log(response);
            }
        });
    },

    getGPIO: function() {
       var completeUrlFront = baseURL + "2" + "/value"; 
       var completeUrlBack = baseURL + "3" + "/value";
       var completeUrlLeft = baseURL + "27" + "/value";
       var completeUrlRight = baseURL + "17" + "/value";
	/*
       var myHeaders = new Headers();

	var myInit = { method: 'GET',
               headers: myHeaders,
               mode: 'no-cors',
               cache: 'default' };
	var myRequest = new Request(completeUrlFront, myInit);

	fetch(myRequest, myInit)
		.then(function(response) {
		gpiofront = response;
		console.log(gpiofront);
	});*/
	
        $.ajax({
            url: completeUrlFront,
            type: 'GET',
            success: function(response) {
                gpiofront = response;
                console.log(gpiofront);
            }
        });
        $.ajax({
            url: completeUrlBack,
            type: 'GET',
            success: function(response) {
                gpioback = response;
            }
        });
        $.ajax({
            url: completeUrlLeft,
            type: 'GET',
            success: function(response) {
                gpioleft = response;
            }
        });
        $.ajax({
            url: completeUrlRight,
            type: 'GET',
            success: function(response) {
                gpioright = response;
            }
        });
    },

    lightHandler: function() {

	var front = $('#light-front');
	var back = $('#light-back');
	var left = $('#light-left');
	var right = $('#light-right'); 

	if(gpiofront == 1) { // change to GET request
            front.removeClass('color-red');
            front.addClass('color-green');
        }
        else {
            front.removeClass('color-green');
            front.addClass('color-red');
        }
        if(gpiofront == 1) { // change to GET request
            front.removeClass('color-red');
            front.addClass('color-green');
        }
        else {
            front.removeClass('color-green');
            front.addClass('color-red');
        }
        if(gpioback == 1) { // change to GET request
            back.removeClass('color-red');
            back.addClass('color-green');
        }
        else {
            back.removeClass('color-green');
            back.addClass('color-red');
        }
        if(gpioleft == 1) { // change to GET request
            left.removeClass('color-red');
            left.addClass('color-green');
        }
        else {
            left.removeClass('color-green');
            left.addClass('color-red');
        }
        if(gpioright == 1) { // change to GET request
            right.removeClass('color-red');
            right.addClass('color-green');
        }
        else {
            right.removeClass('color-green');
            right.addClass('color-red');
        }
    }
};

$(document).ready(function() {
    handlers.getGPIO();
    $('#light-front').click(handlers.postGPIOHandlerFront);
    $('#light-back').click(handlers.postGPIOHandlerBack);
    $('#light-left').click(handlers.postGPIOHandlerLeft);
    $('#light-right').click(handlers.postGPIOHandlerRight);
    setInterval(function(){ 
        handlers.lightHandler();
	handlers.getGPIO();
    }, 2000);

});
