import serial
import time

port = 'COM5'
ser = serial.Serial(port, 9600)
time.sleep(2)

msg = 22

def setTemp(msg):
    if msg.isnumeric():
        if int(msg) <= 40 and int(msg) >= 10:
            serialWrite(msg)
            print("Set temperature: " + msg)
        else:
            print("ERROR: Invalid temperature enter between 10 and 40")
    else:
        print("ERROR: Invalid temperature input")

def onOffArduino(msg):
    if msg == "on":
        serialWrite("on")
        print("Status: " + msg )
    elif msg == "off":
        serialWrite("off")
        print("Status: " + msg )
    else:
        print("ERROR: Invalid input")


def serialWrite(msg):
    ser.write(str.encode(msg))

def sortMsg(msg):
    if "on" or "off" in msg:
        onOffArduino(msg)
    elif msg.isnumeric():
        setTemp(msg)
    else:
        print("ERROR: Invalid input")

try:
    ser.isOpen()
    print("Serial port is open ")

    onOffArduino("on")
    setTemp("10")
except:
    print("Error")
    exit()

# if(ser.isOpen()):
#     try:
#         while(1):
#             line = ser.readline()
#             decodeInput = line.decode('utf-8')
#             print(decodeInput)
#     except:
#         print("Error")