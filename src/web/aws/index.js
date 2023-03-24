// aws handling
var awsIot = require('aws-iot-device-sdk');
var deviceInfo = require('./endpoint.json');


// provided aws identification for a device to connect
// WARNING: giving information of an active client identifier in use will terminate it
var tank = awsIot.device({
    host: deviceInfo.endpoint,
    clientId: 'NerfTank',
    certPath: './certifs/certificate.pem.crt',
    caPath: './certifs/AmazonRootCA1.pem',
    keyPath: './certifs/private.pem.key'
});