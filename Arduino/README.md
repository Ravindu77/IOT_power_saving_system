<h1>IOT_power_saving_system</h1>

<h2>Arduino</h2>

# Temperature
    IdalTemp min : 10
    IdalTemp min : 40

# components
    #LED: Red, Green, Yellow
    #Buttons: 3 Buttons
    #DHT11 Temperatur & Humidity Sensor
    #Resistors: 3 Resistors

# Input pins

    #LEDs
        #Red LED: pin 3
        #Green LED: pin 4
        #Yellow LED: pin 5
    
    #Buttons
        #Power button: pin 2
        #Ideal temperature increase button: pin 10
        #Ideal temperature decrease button: pin 11

# How the Circuit works
    #Purpose of the circuit is to creating a self regulating temperatur controle system
    #Circuit uses LEDs to simulate the temperatur controle
        #Red LED: Heater
        #Green LED: A/C
        #Yellow LED: Power on or off (Blinking LED circuit is off Solid light is power on)
    #Circuit uses serial comunication to connect to the edge device

# Main functions in the arduino Source code
    readSerial()
        Reads seral inputs from the edge device. Gets single string as a input
        If the reading is "on" or "off" sets condition to true or false
        eg:
            "on" - Turn on device
            "off" - Turn off device
            "27" - Sets ideal temperature to 27

        Sub functions
            inputTempCheck(msg): Validation for the temperature input accepts inputs 10 - 40

    readTempHumid()
        #Reads temperature and humidity and update values
        #Serial write to the edge device

    pushButton(buttonState, buttonPin)
        Sets condition with button input and serial write to edge device
        Works as a push button

        Sub functions
            button(state, pin): Button funtion

    tempChange()
        Uses two button inputs to decrease or increase ideal temperatur

        Sub functions
            button(state, pin): Button funtion

    tempControl()
        This function controls A/C and heater

        Sub functions
            heaterOn(): Turns on heater if the temperature is lower than the ideal temperatur
            acOn(): Turns on A/C if the temperature is higher than the ideal temperatur
            acOff(): Turns off both A/C and Heater if the ideal temperature is reached

    allOff()
        Turns off both A/C and Heater if the power button press to turn off device

    blinkY()
        Blink the indicator LED

# How heaterOn() acOn() functions without overlapping A/C and Heater
    Bother functions sets default to turn off other device if one device turns ON
    There for system won't allows both A/C and Heater be on "ON' state
