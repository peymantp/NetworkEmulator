#! python3
import socket
import threading
import hashlib
import time
import datetime
import random
from packet import packet

path = 'config'
configFile = open(path,'r')
configFileLines = configFile.readlines()
emulatorIP = configFileLines[2].replace('\n','').split('=')[1]
emulatorPort = configFileLines[3].replace('\n','').split('=')[1]
dropRate = configFileLines[4].replace('\n','').split('=')[1]
transmitterIP = configFileLines[5].replace('\n','').split('=')[1]
transmitterPort = configFileLines[6].replace('\n','').split('=')[1]
recieverIP = configFileLines[9].replace('\n','').split('=')[1]
recieverPort = configFileLines[10].replace('\n','').split('=')[1]

packetsRecieved = 0
packetsDropped = 0
packetsSent = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((emulatorIP, emulatorPort))

print("server emulator running")
def transmitter(ip,port):
    return

def reciever(ip,port):
    return

while True:
    transmitterThread = threading.Thread(target=transmitter,args=(transmitterIP,transmitterPort))
    recieverThread = threading.Thread(target=reciever,args=(recieverIP,recieverPort))
    transmitterThread.start()
    recieverThread.start()