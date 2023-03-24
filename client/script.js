/*
Author: Kevin Dang
Date: 3-23-2023
File: script.js
Desc: basic scripting file to read in click inputs from the user and send them to the pi

Last Modified: 3-23-2023
*/

// start this upon loading the window
window.onload = function() {
    // movement
    var left_move = document.getElementById("left");
    var right_move = document.getElementById("right");
    var foward_move = document.getElementById("foward");
    var reverse_move = document.getElementById("reverse");

    // add eventlisteners for each interactable
    left_move.addEventListener("click", function() {sendMessage("left")});
    right_move.addEventListener("click", function() {sendMessage("right")});
    foward_move.addEventListener("click", function() {sendMessage("foward")});
    reverse_move.addEventListener("click", function() {sendMessage("reverse")});

    // turret
    var right_aim = document.getElementById("r-aim");
    var left_aim = document.getElementById("l-aim");
    var up_aim = document.getElementById("u-aim");
    var down_aim = document.getElementById("d-aim");
    var fire_round = document.getElementById("fire");

    // listeners for the buttons
    right_aim.addEventListener("click", function() {sendMessage("aim right", right_aim)});
    left_aim.addEventListener("click", function() {sendMessage("aim left")});
    up_aim.addEventListener("click", function() {sendMessage("aim up")});
    down_aim.addEventListener("click", function() {sendMessage("aim down")});
    fire_round.addEventListener("click", function() {sendMessage("fire!")});
}

// simple function to see if it works
function sendMessage(message_to_send) {
    console.log("message from button: " + message_to_send);
}