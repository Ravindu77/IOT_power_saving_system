import serial
import time

port = 'COM5'
ser = serial.Serial(port, 9600)
time.sleep(2)

try:
    ser.isOpen()
    print("Serial port is open")
except:
    print("Error")
    exit()

if(ser.isOpen()):
    try:
        while(1):
            line = ser.readline()
            decodeInput = line.decode('utf-8')
            print(decodeInput)
    except:
        print("Error")