import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

#AWS IoT Connection/Certificates
ENDPOINT = "a3mawz1u3o5d12-ats.iot.ap-southeast-2.amazonaws.com"
CLIENT_ID = "testMqtt"
PATH_TO_CERT = "Certificates/a72e84a361-certificate.pem.crt"
PATH_TO_KEY = "Certificates/a72e84a361-private.pem.key"
PATH_TO_ROOT = "Certificates/AmazonRootCA1.pem"

#Connect to AWS IoT
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

#myAWSIoTMQTTClient.connect()

myAWSIoTMQTTClient.connect()
print("connected")

def topicCallback(client, userdata, message):
    payload = message.payload.decode("utf-8")+"\n"
    print(payload)


while True:
    myAWSIoTMQTTClient.subscribe("publish-topic", 0, topicCallback)