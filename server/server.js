// aws handling
var awsIot = require('aws-iot-device-sdk');
var deviceInfo = require('./endpoint.json');

// vars
var id = "NerfTankInterface";


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
    console.log('Connected to AWS IoT Core');

    // subscribe to other topic, this topic should send device messages
    device.subscribe('from_client');

    var message = "PC client connected with indentity: " + id;
    device.publish('device_connection', JSON.stringify({ message: message }));
});

// receiver method from AWS IoT Core topic, confirms message received
device.on('message', (topic, payload) => {
    console.log('message', topic, payload.toString());
});
