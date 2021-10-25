import serial
import time

port = 'COM5'
ser = serial.Serial(port, 9600)
time.sleep(2)

msg = 22

def setTemp(msg):
    print(msg)
    if msg.isnumeric(msg):
        if int(msg) <= 40 and int(msg) >= 10:
            #serialWrite(msg)
            print(msg)
        else:
            print("ERROR: Invalid temperature enter between 10 and 40")
    else:
        print("ERROR: Invalid temperature input")

def setAuto(msg):
    if msg == "on":
        serialWrite("on")
        print(msg)
    elif msg == "off":
        serialWrite("off")
        print(msg)
    else:
        print("ERROR: Invalid input")

def serialWrite(msg):
    ser.write(str.encode(msg))

setTemp("10")
try:
    ser.isOpen()
    print("Serial port is open ")

    #setAuto("on")
    #setTemp("10")
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