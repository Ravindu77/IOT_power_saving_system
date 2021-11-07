<h1>IOT_power_saving_system</h1>

<h2>Web API</h2> 

# AWS IoT conncetion
- Certificates - provides security certificate and keys generated from AWS IoT core.

- aws-iot-sdk-browser-bundle.js and bundle.js - this package allows to write JavaScript applications which access to AWS IoT Platform via MQTT or MQTT over the Secure WebSocket Protocol.
A new AWS IoT Device SDK is [available] (https://github.com/awslabs/aws-iot-device-sdk-js-v2). 

- home.js - this is the actual JavaScript file for connecting to the AWS IoT Platform. Defining topics for publishing and subscribing to/from the service using MQTT protocol. And provides conditional check to the web API.

- home.html -  The web API for Power-Saving system in HTML format, sending and receiving data to/from AWS IoT Platform.

- css files -  Styling for the web API.

# MQTT Topics
Reading data using Json format.

- Subscription topics          
Topic: "power-topic":
eg: {"date": "2021-10-26 17:51:23", "state": "On"}
    {"date": "2021-10-26 17:51:30", "state": "Off"}

Topic: "tempChange-topic"
eg: {"date": "2021-10-26 17:52:28", "idealTemp": "27.00"}

Topic: "readings-topic"
eg: {"date": "2021-10-26 17:51:25","temp": "25.0", "humid": "51.0"}

Sending data using String format.        
- Publish topic
Topic: "readings-topic"
eg: "on", "off", "35"

# Web API
- The web API provides visualisation and controls to/from the edge devices.
        
1. Toggle switch: turn on/off to the edge devices.
2. Temperture thermostat: to increases and decreases to the edge devices (10-40°C).