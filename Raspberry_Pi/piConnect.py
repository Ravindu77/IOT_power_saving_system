import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import serial
import json
import datetime
import time
from queue import Queue
from threading import Condition, Thread
#DTO class
from dataClasses import Reading, Power, TempChange

#Serial connection setup
port = 'COM5'
ser = serial.Serial(port, 9600)
time.sleep(2)

#AWS IoT Connection/Certificates
ENDPOINT = "a3mawz1u3o5d12-ats.iot.ap-southeast-2.amazonaws.com"
PATH_TO_CERT = "Certificates/a72e84a361-certificate.pem.crt"
PATH_TO_KEY = "Certificates/a72e84a361-private.pem.key"
PATH_TO_ROOT = "Certificates/AmazonRootCA1.pem"


#global variable to run functions or kill function
condition = True

#Set Arduino ideal temp
def setTemp(msg):
    if msg.isnumeric():
        if int(msg) <= 40 and int(msg) >= 10:
            serialWrite(msg)
            print("Set temperature: " + msg)
            q.put(msg)
        else:
            print("ERROR: Invalid temperature enter between 10 and 40")
    else:
        print("ERROR: Invalid temperature input")

#Turn on Arduino
def onOffArduino(msg):
    if msg == "on":
        serialWrite("on")
        print("Status: " + msg )
        q.put(msg)
    elif msg == "off":
        serialWrite("off")
        print("Status: " + msg )
        q.put(msg)
    else:
        print("ERROR: Invalid input")

def sortMsg(msg):
    if "on" == msg or "off" == msg:
        onOffArduino(msg)
    elif msg.isnumeric():
        setTemp(msg)
    else:
        print("ERROR: Invalid input from sortMsg")

#Serial write
def serialWrite(msg):
    ser.write(str.encode(msg))

#Read mqtt messages
def topicCallback(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(payload)
    print(len(payload.strip()))

    msg = str(payload.strip())

    sortMsg(msg)

#Connect to AWS IoT
def connectToMqtt(ClientID):
    client = AWSIoTPyMQTT.AWSIoTMQTTClient(ClientID)
    client.configureEndpoint(ENDPOINT, 8883)
    client.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
    return client

#Get cuttent date and time
def getDateTime():
    x = datetime.datetime.now()
    date = x.strftime('%Y-%m-%d %H:%M:%S')
    print(x.strftime('%Y-%m-%d %H:%M:%S'))
    return date

#DTO Classes setup
#Check the string is a float
#Arduino send float values for temperature
def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

#Split the serial reading from arduino
def splitDecodeInput(decodeInput, date, client):
    splitInput = decodeInput.split(" ")
    jsonStr = ""

    if len(splitInput) > 2:
        jsonStr = readingsToJson(splitInput, date)
        client.publish("readings-topic", jsonStr, 1)
    else:
        temp = splitInput[0]

        if check_float(temp):
            jsonStr = tempChangeToJson(temp, date)
            #client.publish("readings-topic", jsonStr, 1)
            #tempChange-topic
            client.publish("tempChange-topic", jsonStr, 1)
        else:
            jsonStr = powerToJson(temp, date)
            #client.publish("readings-topic", jsonStr, 1)
            #power-topic
            client.publish("power-topic", jsonStr, 1)
    
#json translation
def readingsToJson(splitInput, date):
    temp = splitInput[1]
    humid = splitInput[3]
    
    reading = Reading(date, temp, humid)
    return json.dumps(reading.__dict__)

def powerToJson(status, date):
    power = Power(date, status)
    return json.dumps(power.__dict__)

def tempChangeToJson(status, date):
    tempChange = TempChange(date, status)
    return json.dumps(tempChange.__dict__)


#Start Thread
def serialListner(input_queue, clientID):
    global condition
    client = connectToMqtt(clientID)
    client.connect()

    while condition:
        try:
            line = ser.readline()
            decodeInput = line.decode('utf-8')
            print(decodeInput)
            jsonStr = splitDecodeInput(decodeInput, getDateTime(), client)
        except:
            print("ERROR: Reading serial input")
    
    client.disconnect()

def mqttListner(input_queue, clientID, topic):
    global condition
    client = connectToMqtt(clientID)
    client.connect()

    while condition:
        client.subscribe(topic, 0, topicCallback)
    
    client.disconnect()

#For internal communication between Thread uses the "q" queue
#Purpouse of this function is to read the messages in the queue and publish it to the topics
def internalQueueReader(input_queue, clientID):
    global condition
    client = connectToMqtt(clientID)
    client.connect()

    while condition:
        if not input_queue.empty():
            data = input_queue.get()
            splitDecodeInput(data, getDateTime(), client)
            input_queue.task_done()
    
    client.disconnect()

def cliHandler(input_queue):
    global condition
    strInput = str(input())

    print("Arduino and AWS mqtt disconnected")
    condition = False

#End Thread


q = Queue()
t1 = Thread(target=serialListner, args=(q, "Client01"))
t2 = Thread(target=mqttListner, args=(q, "Client02", "publish-topic"))
t3 = Thread(target=internalQueueReader, args=(q, "Client03"))
t4 = Thread(target=cliHandler, args=(q,))

t1.start()
t2.start()
t3.start()
t4.start()