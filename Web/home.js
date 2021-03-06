/*
 * Copyright 2015-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

//
// Instantiate the AWS SDK and configuration objects.  The AWS SDK for 
// JavaScript (aws-sdk) is used for Cognito Identity/Authentication, and 
// the AWS IoT SDK for JavaScript (aws-iot-device-sdk) is used for the
// WebSocket connection to AWS IoT and device shadow APIs.
// 
var AWS = require('aws-sdk');
var AWSIoTData = require('aws-iot-device-sdk');

console.log('Loaded AWS SDK for JavaScript and AWS IoT SDK for Node.js');

//
// Remember our current subscription topic here.
//
var currentlySubscribedTopic = 'readings-topic';
var currentlySubscribedTopic2 = 'tempChange-topic';
var currentlySubscribedTopic3 = 'power-topic';
//
// Create a client id to use when connecting to AWS IoT.
//
var clientId = 'mqtt-explorer-g3';

//
// Initialize our configuration.
//
AWS.config.region = 'ap-southeast-2';

AWS.config.credentials = new AWS.CognitoIdentityCredentials({
   IdentityPoolId: 'ap-southeast-2:3bba12e9-4d41-45dc-8dd6-299dbd1f13b3'
});

//
// Create the AWS IoT device object.  Note that the credentials must be 
// initialized with empty strings; when we successfully authenticate to
// the Cognito Identity Pool, the credentials will be dynamically updated.
//
const mqttClient = AWSIoTData.device({
   //
   // Set the AWS region we will operate in.
   //
   region: AWS.config.region,
   //
   ////Set the AWS IoT Host Endpoint
   host: 'a3mawz1u3o5d12-ats.iot.ap-southeast-2.amazonaws.com',
   //
   // Use the clientId created earlier.
   //
   clientId: clientId,
   //
   // Connect via secure WebSocket
   //
   protocol: 'wss',
   //
   // Set the maximum reconnect time to 8 seconds; this is a browser application
   // so we don't want to leave the user waiting too long for reconnection after
   // re-connecting to the network/re-opening their laptop/etc...
   //
   maximumReconnectTimeMs: 8000,
   //
   // Enable console debugging information (optional)
   //
   debug: false,
   //
   // IMPORTANT: the AWS access key ID, secret key, and sesion token must be 
   // initialized with empty strings.
   //
   accessKeyId: '',
   secretKey: '',
   sessionToken: ''
});

//
// Attempt to authenticate to the Cognito Identity Pool.  Note that this
// example only supports use of a pool which allows unauthenticated 
// identities.
//
var cognitoIdentity = new AWS.CognitoIdentity();
AWS.config.credentials.get(function(err, data) {
   if (!err) {
      console.log('retrieved identity: ' + AWS.config.credentials.identityId);
      var params = {
         IdentityId: AWS.config.credentials.identityId
      };
      cognitoIdentity.getCredentialsForIdentity(params, function(err, data) {
         if (!err) {
            //
            // Update our latest AWS credentials; the MQTT client will use these
            // during its next reconnect attempt.
            //
            mqttClient.updateWebSocketCredentials(data.Credentials.AccessKeyId,
               data.Credentials.SecretKey,
               data.Credentials.SessionToken);
         } else {
            console.log('error retrieving credentials: ' + err);
            alert('error retrieving credentials: ' + err);
         }
      });
   } else {
      console.log('error retrieving identity:' + err);
      alert('error retrieving identity: ' + err);
   }
});

//
// Connect handler; update div visibility and fetch latest shadow documents.
// Subscribe to lifecycle events on the first connect event.
//
window.mqttClientConnectHandler = function() {
   console.log('connect');
   document.getElementById("connecting-div").style.visibility = 'hidden';
   document.getElementById("explorer-div").style.visibility = 'visible';
   document.getElementById('date-div').innerHTML = '';
   document.getElementById('temp-div').innerHTML = '';
   document.getElementById('humid-div').innerHTML = '';

   //
   // Subscribe to our current topic.
   //
   mqttClient.subscribe(currentlySubscribedTopic);
   mqttClient.subscribe(currentlySubscribedTopic2);
   mqttClient.subscribe(currentlySubscribedTopic3);
};

//
// Reconnect handler; update div visibility.
//
window.mqttClientReconnectHandler = function() {
   console.log('reconnect');
   document.getElementById("connecting-div").style.visibility = 'visible';
   document.getElementById("explorer-div").style.visibility = 'hidden';
};

//
// Utility function to determine if a value has been defined.
//
window.isUndefined = function(value) {
   return typeof value === 'undefined' || typeof value === null;
};

//
// Message handler for lifecycle events; create/destroy divs as clients
// connect/disconnect.
//
window.mqttClientMessageHandler = function(topic, payload) {
   console.log('message: ' + topic + ':' + payload.toString());
   if(topic ==='readings-topic'){
	  var obj_readings_topic = JSON.parse(payload.toString());
      var date = obj_readings_topic.date;
      var temp = obj_readings_topic.temp;
      var humid = obj_readings_topic.humid;
	  document.getElementById('date-div').innerHTML = date ;
	  document.getElementById('temp-div').innerHTML = temp+'??C' ;
	  document.getElementById('humid-div').innerHTML = humid+'%' ;
	  if(obj_readings_topic){
		  document.getElementById('publish-data').checked = true;
	  }
	  if(obj_readings_topic == false){
		  document.getElementById('publish-data').checked = false;
	  }
   }
   if(topic ==='tempChange-topic'){
	  var obj_tempChange_topic = JSON.parse(payload.toString());
	  var idealtemp = obj_tempChange_topic.idealTemp;
	  document.getElementById('publish-data1').value = idealtemp+'??C' ;
   }
   if(topic ==='power-topic'){
	  var obj_power_topic = JSON.parse(payload.toString());
	  var state = obj_power_topic.state;
	  if(state==='on'){
		  document.getElementById('publish-data').checked = true;
	  }
	  if(state ==='off'){
		  document.getElementById('publish-data').checked = false;
		  document.getElementById('date-div').innerHTML = '';
		  document.getElementById('temp-div').innerHTML = '';
		  document.getElementById('humid-div').innerHTML = '';
	  }
   }
  if (obj_readings_topic && obj_tempChange_topic && obj_power_topic) {
     //do database update or print
      console.log("----");
      console.log("obj_readings-topic: %s", obj_readings_topic);
      console.log("----");
      console.log("obj_tempChange-topic: %s", obj_tempChange_topic);
      console.log("----");
      console.log("obj_power-topic: %s", obj_power_topic);
      //reset to undefined for next time
      obj_readings_topic = undefined;
      obj_tempChange_topic = undefined;
	  obj_power_topic = undefined;
  }

};


//
// Handle the UI for the current topic subscription
//
window.updateSubscriptionTopic = function() {
   var subscribeTopic = document.getElementById('subscribe-topic').value;
   document.getElementById('date-div').innerHTML = '';
   document.getElementById('temp-div').innerHTML = '';
   document.getElementById('humid-div').innerHTML = '';
   mqttClient.unsubscribe(currentlySubscribedTopic);
   currentlySubscribedTopic = subscribeTopic;
   mqttClient.subscribe(currentlySubscribedTopic);
};

//
// Handle the UI to update the topic we're publishing on
//
window.updatePublishTopic = function() {};

//
// Handle the UI to update the data we're publishing
//
window.updatePublishData = function() {
   var checked_data = document.getElementById('publish-data').checked;
   var publishTopic = '';
   var publishText = '';

	if(checked_data == false){
		publishTopic = "publish-topic";
	    publishText = "off";
	}
	if(checked_data == true){
		publishTopic = "publish-topic";
	    publishText = "on";
	}


   mqttClient.publish(publishTopic, publishText);

};

window.increaseValue = function() {
  var value = parseInt(document.getElementById('publish-data1').value, 10);
  if(value<40){
     value = isNaN(value) ? 0 : value;
     value++;
     document.getElementById('publish-data1').value = value+"??C";
     mqttClient.publish("publish-topic", value.toString());
  }else{
	  document.getElementById('publish-data1').value = "40??C";
  }


}

window.decreaseValue = function() {
  var value = parseInt(document.getElementById('publish-data1').value, 10);
  if(value>10){
	 value = isNaN(value) ? 0 : value;
     value < 1 ? value = 1 : '';
     value--;
     document.getElementById('publish-data1').value = value+"??C";
     mqttClient.publish("publish-topic", value.toString());
  }else{
	  document.getElementById('publish-data1').value = "10??C";
  }

}

//
// Install connect/reconnect event handlers.
//
mqttClient.on('connect', window.mqttClientConnectHandler);
mqttClient.on('reconnect', window.mqttClientReconnectHandler);
mqttClient.on('message', window.mqttClientMessageHandler);

//
// Initialize divs.
//
document.getElementById('connecting-div').style.visibility = 'visible';
document.getElementById('explorer-div').style.visibility = 'hidden';
document.getElementById('connecting-div').innerHTML = '<p>attempting to connect to aws iot...</p>';
