// handle requirements
const express = require('express');
const cors = require('cors');
const createError = require('http-errors')

// aws requirements
var awsIot = require('aws-iot-device-sdk');
var deviceInfo = require('./endpoint.json');

// variables for client and aws
let id = "NerfTankInterface";
const PORT = process.env.PORT || 8080;

// ---------------------------------------------------------------------
// AWS Connection Setup
// ---------------------------------------------------------------------

// provided aws identification for a device to connect
// WARNING: having the same clientId of an active client identifier in use will terminate/replace it
var device = awsIot.device({
    host: deviceInfo.endpoint,
    clientId: id,
    certPath: './certifs/certificate.pem.crt',
    caPath: './certifs/AmazonRootCA1.pem',
    keyPath: './certifs/private.pem.key'
});

// connection to AWS IoT Core
device.on('connect', () => {
    console.log('Connecting to AWS IoT Core');

    device.subscribe('from_client');

    // subscribe to other topic, this topic should send device messages
    var message = "PC client connected with indentity: " + id;
    device.publish('device_connection', JSON.stringify({ message: message }));
});

// receiver method from AWS IoT Core topic, confirms message received
device.on('message', (topic, payload) => {
    console.log('message', topic, payload.toString());
});

// ---------------------------------------------------------------------
// Express Setup
// ---------------------------------------------------------------------

// set up url connection
const app = express();
app.use(express.json()); // expect json request
app.use(cors());

app.post('/sendMessage', async (request, response, next) => {
    try {
        // get the information and send it
        const result = request.body;
        console.log(`This is what we got: ${result.command}`)
        device.publish('from_client', JSON.stringify({ command: result.command }));
    } catch (err) {
        next(err);
    }
})

// invalid url types
app.use(async (request, response, next) => {
    console.error('Invalid access to a route, ERROR', 404);
    next(createError.NotFound('This route was not found'));
});

// sends error response to interface
app.use((err, request, response, next) => {
    response.status(err.status || 500);
    response.send({
        error: {
            status: err.status || 500,
            message: err.message
        }
    });
});

// allows to access this server
app.listen(PORT, () => {
    console.log(`Server listening on https://localhost:${PORT}`);
})