#! python3
import argparse
import os
import socket
import sys
import time, datetime
from os import path

from config_helper import ConfigHelper as conf
from packet import packet

#reading from config file
config = conf("config")
emulatorAddress = config.getEmulartor()
recieverAddress = config.getReciever()

packetsRecieved = {} #used to check if a packet has been recieved more than once
packetsACK = {} #used to check if an ACK has been sent more than once
EOT = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(recieverAddress)


def duplicationCheckRecieved(packetArray):
    """
    Function checks a dictonary of key:sequence number and value:number of times recieved\n
    If value is None packet is not a duplicate\n
    If value is not None incriment by one\n
    Returns True for duplicate and False original
    """
    duplicate = False
    seq = packetArray[1]
    packetsRecievedValue = packetsRecieved.get(seq)
    if packetsRecievedValue is None:
        packetsRecieved[seq] = 1
        return duplicate
    else:
        duplicate = True
        packetsRecieved[seq] = packetsRecievedValue + 1
        return duplicate

def duplicationCheckSent(packetArray):
    duplicate = False
    ack = packetArray[3]
    packetsSentValue = packetsACK.get(ack)
    if packetsSentValue is None:
        packetsACK[ack] = 1
        return duplicate
    else:
        duplicate = True
        packetsACK[ack] = packetsSentValue + 1
        return duplicate

def send(pacArray):
    pac = packet(1,pacArray[1],pacArray[2],pacArray[3])
    pacString = pac.toString()
    if duplicationCheckSent(pacArray):
        recieverLog.write("resending "+pacString+"\n")
    else:
        recieverLog.write("sending "+pacString+"\n")
    data = pacString.encode()
    s.sendto(data,emulatorAddress)

def EOTfunction(pacArray):
    pac = packet(3,pacArray[1],pacArray[2],pacArray[3])
    pacString = pac.toString()
    if duplicationCheckSent(pacArray):
        recieverLog.write("resending "+pacString+"\n")
    else:
        recieverLog.write("sending "+pacString+"\n")
    data = pacString.encode()
    s.sendto(data,emulatorAddress)

#log file creation
time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
recieverLog = open("recieverLog"+time+".md",'w+')
filebuffer = []
filename = 'recievedfile_'+time
while not EOT:
    data = s.recv(1024)
    data = data.decode()
    packetData = packet.parse(data)
    packetData = list(packetData)
    print(packetData)
    if packetData[0] == '3': #if EOT packet
        print("### EOT \n" + data)
        recieverLog.write("### EOT \n" + data)
        EOTfunction(packetData)
        recieverLog.close()
        EOT = True
    elif packetData[0] == '0': #if data packet
        if duplicationCheckRecieved(packetData): #if packet is a duplicate
            print("recieved duplicate "+data+"\n")
            recieverLog.write("**recieved duplicate** "+data+"\n")
            send(packetData)
        else:
            print("recieved "+data+"\n")
            recieverLog.write("recieved "+data+"\n")
            send(packetData)
exit()
