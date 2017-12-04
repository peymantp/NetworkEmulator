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

pac = packet(1,0,2048,1) #initil packet
packetsRecieved = {}
packetsACK = {}
EOT = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(recieverAddress)
time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
recieverLog = open("recieverLog"+time+".md",'x')

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

#def duplicationCheckSent(packet: packetObj):
#    retuen

while not EOT:
    data = s.recv()
    packetData = packet.parse(data)
    if packetData[0] == 3: #if EOT packet
        recieverLog.write("### EOT \n" + data)
        recieverLog.close()
        EOT = True
    elif packetData[0] == 2: #if SOT packet
        if duplicationCheckRecieved(packetData): #if packet is a duplicate
            recieverLog.write("recieved duplicate**"+data+"**\n")
        else:
            recieverLog.write("### SOT \n" + data)
        _file = open(packetData[4],'x')
    elif packetData[0] == 0: #if data packet
        if duplicationCheckRecieved(packetData): #if packet is a duplicate
            recieverLog.write("recieved duplicate**"+data+"**\n")
        else:
            recieverLog.write("recieved"+data+"\n")
            _file.write(packetData[4])

sys.exit()
