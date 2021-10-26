<h1>IOT_power_saving_system</h1>

<h2>Raspberry Pi</h2>

# libraries 
    pip install AWSIoTPythonSDK
    python -m pip install pyserial
    pip install threaded

# For windows users if venv doesn't work try this command
    Set-ExecutionPolicy Unrestricted -Scope Process
    .\.venv\scripts\activate

# Communication methods
    # Serial
        #Purpouse: To connect arduino and edge device (Raspberi pi or PC)
    # mqtt
        #Purpouse: To connect and comunicate between server and edge device

# How to send send messages to the edge devicee
    #Edge device recives messages in <String> format
        Topic: "publish-topic"
        #Commands
            #Turn on device: on
            #Turn on device: off
            #To change ideal temperature: 28
            (Device accepts ideal temperature readings between 10 - 40 degrees)

# How to read messages sends by the edge device
    #Edge device send messages in a json format
    #DTO class(Reference: dataClasses.py)
        #Uses three data class to store data and read data
        #By creating a object using this json input will be able to access data easily
         eg: reading = json.loads(jsonStr, object_hook=Reading)

        #Reading
            Topic: "readings-topic"
            eg: {"date": "2021-10-26 17:51:25", "temp": "25.0", "humid": "51.0"}
        #Power
            Topic: "power-topic"
            eg: on: {"date": "2021-10-26 17:51:23", "state": "On"}
                off: {"date": "2021-10-26 17:51:30", "state": "Off"}
        #TempChange
            Topic: "tempChange-topic"
            eg: {"date": "2021-10-26 17:52:28", "idealTemp": "27.00"}


# Threads
    #serialListner
        #ClientID: Client01
        #Topics: readings-topic, power-topic, tempChange-topic
        #Purpouse: Purpouse of this function is to run as an active serial listner thread

    #mqttListner
        #ClientID: Client02
        #Topics:publish-topic

    #cliHandler
        #Purpouse: Two threads I mentioned above uses while loop with a coundition check to run #this function let developer to give a keyboard input to distrupt threads by changing #the condition to false