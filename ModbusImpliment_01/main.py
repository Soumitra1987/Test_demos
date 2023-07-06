# This is a sample Python script.

import socket
import serial
import keyboard
import time

#     if Mode = 1 then it is serial or Mode =2 then it is TCPIP
Mode = int(input("Enter the Mode:"))


def ser1():
    COM = str(input("Enter the COM PORT Number:"))
    Baud = int(input("Enter the Buadrate:"))
    ser = serial.Serial(COM, Baud, timeout=1)

    while True:
        time.sleep(5)
        # Read holding register 0x00 from slave 1
        request = b'\x01\x03\x00\x00\x00\x01\x84\x0A'
        ser.write(request)
        response = ser.read(5)

        print(response)

        if keyboard.is_pressed("Q"):
            print("User want to Quit")
            break
        # print("Connected")

    ser.close()


def TCP1():
    # create a socket object
    modtcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = str(input("Enter host TcpIP/address:"))

    port = 502

    # connection to hostname on the port.
    modtcp.connect((host, port))

    while True:
        time.sleep(2)

        # send data to the server
        modtcp.sendall(b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x01')

        # receive data from the server
        data = modtcp.recv(1024)

        print((data))

        if keyboard.is_pressed("Q"):
            print("User want to Quit")
            break
        print("Connected")


if Mode == 1:  # serial connection
    print("Serial mode Selected")
    ser1()

elif Mode == 2:  # TCP connection
    print("ModbusTcpIP mode Selected")
    TCP1()
