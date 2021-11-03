import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import json
from queue import Queue
from threading import Condition, Thread
#DTO class
from dataClasses import Reading, Power, TempChange

#AWS IoT Connection/Certificates
ENDPOINT = "a3mawz1u3o5d12-ats.iot.ap-southeast-2.amazonaws.com"
PATH_TO_CERT = "Certificates/a72e84a361-certificate.pem.crt"
PATH_TO_KEY = "Certificates/a72e84a361-private.pem.key"
PATH_TO_ROOT = "Certificates/AmazonRootCA1.pem"


#global variable to run functions or kill function
condition = True

#Read mqtt messages
def readingTopicCallback(client, userdata, message):
    payload = message.payload.decode("utf-8")
    #print(payload)
    reading = Reading.from_json(payload)
    print("Date: " + reading.date + " Temp: " + reading.temp + " Humid: " + reading.humid)
    #ADD ur sql here use object reading

def powerTopicCallback(client, userdata, message):
    payload = message.payload.decode("utf-8")
    #print(payload)
    power = Power.from_json(payload)
    print("Date: " + power.date + " Status: " + power.state)
    #ADD ur sql here use object power

def tempChangeTopicCallback(client, userdata, message):
    payload = message.payload.decode("utf-8")
    #print(payload)
    tempChange = TempChange.from_json(payload)
    print("Date: " + tempChange.date + " Ideal Temp : " + tempChange.idealTemp)
    #ADD ur sql here use object tempChange



#Connect to AWS IoT
def connectToMqtt(ClientID):
    client = AWSIoTPyMQTT.AWSIoTMQTTClient(ClientID)
    client.configureEndpoint(ENDPOINT, 8883)
    client.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
    return client

#Start Thread
def readingTopic(input_queue, clientID, topic):
    global condition
    client = connectToMqtt(clientID)
    client.connect()

    while condition:
        client.subscribe(topic, 0, readingTopicCallback)
    
    client.disconnect()

def powerTopic(input_queue, clientID, topic):
    global condition
    client = connectToMqtt(clientID)
    client.connect()

    while condition:
        client.subscribe(topic, 0, powerTopicCallback)
    
    client.disconnect()

def tempChangeTopic(input_queue, clientID, topic):
    global condition
    client = connectToMqtt(clientID)
    client.connect()

    while condition:
        client.subscribe(topic, 0, tempChangeTopicCallback)
    
    client.disconnect()

def cliHandler(input_queue):
    global condition
    strInput = str(input())

    print("End program")
    condition = False

#End Thread
q = Queue()
t1 = Thread(target=readingTopic, args=(q, "sqlClient01", "readings-topic"))
t2 = Thread(target=powerTopic, args=(q, "sqlClient02", "power-topic"))
t3 = Thread(target=tempChangeTopic, args=(q, "sqlClient03", "tempChange-topic"))
t4 = Thread(target=cliHandler, args=(q,))

t1.start()
t2.start()
t3.start()
t4.start()