# This is a sample Python script.

import socket
import serial
import struct
import keyboard
import time

#     if Mode = 1 then it is serial or Mode =2 then it is TCPIP
Mode = int(input("Enter the Mode:"))


'''def Modbusparameters(self,unitID,funion):
    # Set the Modbus parameters
    unitId = 16
    functionCode = 3  # Read Holding Registers
    startAddress = 40010 - 1  # Subtract 1 because Modbus addresses start at 0
    numRegisters = 1

    # Create the Modbus request
    req = struct.pack('>HHHBBHH', 0, 0, 6, unitId, functionCode, startAddress, numRegisters)

    # Send the request to the Modbus device
    sock.send(req)

    # Receive the response from the Modbus device
    response = sock.recv(1024)

    # Unpack the response to get the register value
    header, data = response[:7], response[7:]
    values = struct.unpack('>' + 'H' * numRegisters, data[2:])

    # Print the register value
    print(values)'''



def ser1():
    COM = str(input("Enter the COM PORT Number:"))
    Baud = int(input("Enter the Buadrate:"))
    ser = serial.Serial(COM, Baud, timeout=1)

    while True:

        # Read holding register 0x00 from slave 1
        unitId = 1
        functionCode = 3  # Read Holding Registers
        startAddress = 40002 - 1  # Subtract 1 because Modbus addresses start at 0
        numRegisters = 2

        # Create the Modbus request
        request = struct.pack('>HHHBBHH', 0, 0, 6, unitId, functionCode, startAddress, numRegisters)

        # Send the request to the Modbus device
        ser.write(request)

        # Receive the response from the Modbus device
        response = ser.read(8)

        # Unpack the response to get the register value
        header, data = response[:7], response[7:]
        values = struct.unpack('>' + 'H'* numRegisters, data[2:])

        # Print the register value
        print(values)

        time.sleep(2)

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
        unitId = 1
        functionCode = 3  # Read Holding Registers
        startAddress = 40010 - 1  # Subtract 1 because Modbus addresses start at 0
        numRegisters = 1

        # Create the Modbus request
        request = struct.pack('>HHHBBHH', 0, 0, 6, unitId, functionCode, startAddress, numRegisters)

        # Send the request to the Modbus device
        modtcp.send(request)

        # Receive the response from the Modbus device
        response = modtcp.recv(1024)

        # Unpack the response to get the register value
        header, data = response[:7], response[7:]
        values = struct.unpack('>' + 'H' * numRegisters, data[2:])

        # Print the register value
        print(values)

        # receive data from the server

        if keyboard.is_pressed("Q"):
            print("User want to Quit")
            break
        print("Connected")
    modtcp.close()


if Mode == 1:  # serial connection
    print("Serial mode Selected")
    ser1()

elif Mode == 2:  # TCP connection
    print("ModbusTcpIP mode Selected")
    TCP1()
