#import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
#from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

#AWS IoT Connection/Certificates
ENDPOINT = "ap-southeast-2:3bba12e9-4d41-45dc-8dd6-299dbd1f13b3"
CLIENT_ID = "testMqtt"
PATH_TO_CERT = "Certificates/cb8427d0b9084528740774219ef14573f9e1ca62331090bd893e77abd848775e-certificate.pem.crt"
PATH_TO_KEY = "Certificates/cb8427d0b9084528740774219ef14573f9e1ca62331090bd893e77abd848775e-private.pem.key"
PATH_TO_ROOT = "Certificates/AmazonRootCA1.pem"

#Connect to AWS IoT
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

myAWSIoTMQTTClient.connect()

# try:
#     myAWSIoTMQTTClient.connect()
# except:
#     print("Failed to connect")
#     exit()