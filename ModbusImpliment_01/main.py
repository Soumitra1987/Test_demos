# This is a sample Python script.
import socket
import serial
import struct
import keyboard
import time

#     if Mode = 1 then it is serial or Mode =2 then it is TCPIP
Mode = int(input("Enter the Mode:"))


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc


class Modbuscomms():
    def Sendpacket(self, slaveID, functionCode, startingAddress, registerCount):
        request = struct.pack('>HHHBBHH', 0, 0, 6, slaveID, functionCode, startingAddress, registerCount)
        if Mode == 1:
            crc = crc16(request)
            request += struct.pack('<H', crc)
            return request
        else:
            return request

    def Recivepacket(self, response, registerCount):
        # Unpack the response to get the register value
        header, data = response[:7], response[7:]
        values = struct.unpack('>' + 'H' * registerCount, data[2:])

        # Print the register value
        return values



def ser1():
    COM = str(input("Enter the COM PORT Number:"))
    Baud = int(input("Enter the Buadrate:"))
    ser = serial.Serial(COM, Baud, timeout=1)

    while True:

        # Read holding register 0x00 from slave 1
        unitId = 1
        fCode = 3  # Read Holding Registers
        RAddress = 40002 - 1  # Subtract 1 because Modbus addresses start at 0
        numRegisters = 1

        Modbuscomms1 = Modbuscomms()
        # Create the Modbus request
        request = Modbuscomms1.Sendpacket(unitId, fCode, RAddress, numRegisters)

        # Send the request to the Modbus device
        ser.write(request)

        # Receive the response from the Modbus device
        response = ser.read(5 + 2 * numRegisters)
        values = Modbuscomms1.Recivepacket(response, numRegisters)
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
        fCode = 3  # Read Holding Registers
        RAddress = 40010 - 1  # Subtract 1 because Modbus addresses start at 0
        numRegisters = 10

        Modbuscomms1 = Modbuscomms()
        # Create the Modbus request
        request = Modbuscomms1.Sendpacket(unitId, fCode, RAddress, numRegisters)

        # Send the request to the Modbus device
        modtcp.send(request)

        # Receive the response from the Modbus device
        response = modtcp.recv(1024)
        values = Modbuscomms1.Recivepacket(response, numRegisters)

        # Print the register value
        print(values)

        # receive data from the server

        if keyboard.is_pressed("Q"):
            print("User want to Quit")
            break
        print("Connected")
    modtcp.close()


if Mode == 1:  # serial connection
    print("Modbus Serial mode Selected")
    ser1()

elif Mode == 2:  # TCP connection
    print("ModbusTcpIP mode Selected")
    TCP1()
