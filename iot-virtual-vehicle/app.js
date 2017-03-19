'use strict';

var crypto = require('crypto');
var bs58 = require('bs58');

var clientFromConnectionString = require('azure-iot-device-mqtt').clientFromConnectionString;
var Message = require('azure-iot-device').Message;
var Request = require('request');

// TODO: ETL Logic app URL - this is only needed if data needs to be retrieved from an external source
// using the ETL Logic App 
var etlLogicAppUrl = '<<LOGIC_APP_EXTERNAL_ACCESS_URL>>';

// simulate two different IoT devices (using the client connection string taken from IoT hub registry)
var connectionStringVehicle1 = '<<AZURE_IOT_HUB_DEVICE_CONNECTIONSTRING>>'; 

// TODO: make sure you use the correct IoT hub client connection string
var connectionString = connectionStringVehicle1;
var client = clientFromConnectionString(connectionString);

function printResultFor(op) {
    return function printResult(err, res) {
        if (err) console.log(op + ' error: ' + err.toString());
        if (res) console.log(op + ' status: ' + res.constructor.name);
    };
}

// retrieve the correct objectno from the connection string
// Important: if this should work the registered IoT hub client devices have to have 
// the same name. 
function getVehicleId() {
    // return e.g. '001' -- objectno
    return connectionString.split(';')[1].split('=')[1];
}

// generate the device's public key. This is used by the BigchainDB
// if the Logic App (ETL) will be used, this will be done in the referenced Azure function
// This is only needed if custom data will be sent to the IoT hub
function generateVehiclePublicKey(vehicleId) {
    return bs58.encode(crypto.createHash('sha256').update(vehicleId).digest());
}

// trigger the Azure Logic App. This performs an ETL operation (retrieves and modifies the TomTom data) 
function getTelemtryData(objectno, actionName, callback) {

    // TODO: update the requestParams if needed
    // the correct params are dependent on the TomTom service (actionType) that will be called
    // more information can be found in the TomTom API documentation
    var requestParams = {
        'extractAction': actionName,
        "objectno": objectno,
        'OptionalQueryParams': [
            { 'Key': 'objectno', 'Value': objectno },
            { 'Key': 'year', 'Value': '2017' },
            { 'Key': 'month', 'Value': '02' }
        ],
        'performLoad': false,
        'loadUrl': ''
    }
    
    Request({
        method: 'POST',
        // TODO: make sure you replace this with the Logic App url
        uri: etlLogicAppUrl,
        json: requestParams
    }, function(error, response, body) {
        callback(body);
    });
}

// Produces fake telemetry data to simulate vehicle data
function createTelemetryData() {
    // TODO: implement if needed
}

var connectCallback = function (err) {
if (err) {
        console.log('Could not connect: ' + err);
} else {
        console.log('Client connected');

        var vehicleId = getVehicleId();
        // TODO: specify the operation of the TomTom service that should be called. 
        // the operation names can be found in the TomTom API documentation
        var actionType = 'getTrips';

        // bulk load existing data - 
        var bulkData = getTelemtryData(vehicleId, actionType, function(responseObject) {

            for (let i = 0; i < responseObject.length; i++) {
                setTimeout(function(x) { 
                    return function() {                        
                        let json = JSON.stringify(responseObject[i]);
                        console.log("Sending message: " + json);
                        
                        var message = new Message(json);
                        client.sendEvent(message, printResultFor('send')) 
                    }; 
                }(i), i * 5000);
            }
        });

        // // TODO: Uncomment if regular fake vehicle telemetry data is needed (not taken from the TomTom service) 
        // // Create a message and send it to the IoT Hub every second
        // setInterval(function(){
        //     var message = new Message(createTelemetryData());

        //     console.log("Sending telemetry message: " + message.getData());
        //     client.sendEvent(message, printResultFor('send'));
        // }, 1000);
    }
};

client.open(connectCallback);