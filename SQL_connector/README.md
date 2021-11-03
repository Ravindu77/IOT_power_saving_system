<h1>IOT_power_saving_system</h1>

<h2>SQL Connector</h2>

# libraries 
    pip install AWSIoTPythonSDK
    python -m pip install pyserial
    pip install threaded

# For windows users if venv doesn't work try this command
    Set-ExecutionPolicy Unrestricted -Scope Process
    .\.venv\scripts\activate

#Purpose of this program is to listen to messages published by the devices

# How to read messages sends by the edge device
    #Edge device send messages in a json format
    #DTO class(Reference: dataClasses.py)
        #Uses three data class to store data and read data
        #By creating a object using this json input will be able to access data easily
         eg: reading = Reading.from_json(jsonStr)

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
    #readingTopic
        #ClientID: sqlClient01
        #Topic: readings-topic
    #powerTopic
        #ClientID: sqlClient02
        #Topic: power-topic
    #tempChangeTopic
        #ClientID: sqlClient03
        #Topic: tempChange-topic
    #cliHandler
        #Purpouse: Two threads I mentioned above uses while loop with a coundition check to run #this function let developer to give a keyboard input to distrupt threads by changing #the condition to false
        #If u want to exit the program just type something and hit enter