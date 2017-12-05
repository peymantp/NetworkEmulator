#! python3
import datetime, time
import socket
from itertools import tee

from config_helper import ConfigHelper as conf
from packet import packet

#reading from config file
config = conf("config")
emulatorAddress = config.getEmulartor()
transmitterAddress = config.getTransmitter()
# creating sockets
transmitterSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
transmitterSocket.bind(transmitterAddress)
#log file
time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
transmitterLog = open("transmitterLog"+time+".md",'w+')

WINDOWSIZE = 5
RETRANSMIT = 200
PACKETLIMIT = 50
TIMEOUT = RETRANSMIT*6
BYTESREAD = 1024
seqNumArray = []
ackNumArray = []
data = []
window = []
ack = 0
EOT = False

def packetCreation():
    for var in list(range(PACKETLIMIT)):
        pac = packet(0, var, WINDOWSIZE, var)
        packetstring = pac.toString()
        data.append(packetstring)
        #print(packetstring+"\n") #debug line
    pac = packet(3, PACKETLIMIT, WINDOWSIZE, PACKETLIMIT)
    packetstring = pac.toString()
    #print(packetstring+"\n") #debug line
    data.append(packetstring)

#https://stackoverflow.com/a/6822907
def prepWindow():
    if len(data) < WINDOWSIZE:
        i = len(data)
        for var in list(range(len(data))):
            window.append(data[var])
    else:
        i = WINDOWSIZE
        for var in list(range(WINDOWSIZE)):
            window.append(data[var])

def EOT(pac):
    _sendPacket = pac.encode()
    transmitterSocket.sendto(_sendPacket,emulatorAddress)
    print("sent"+pac+"\n")
    transmitterLog.write("sent"+pac+"\n")

def moveWindow(pac):
    for var in range(len(window)):
        if len(data) < var+1: 
            break
        else:
            tempPacket = data[var]
            tempPacketArray = packet.parse(tempPacket)
            if tempPacketArray[1] == pac[1]:
                del data[var]

packetCreation()
l=0
while len(data) > 0: #send while data is not empty
    try:
        prepWindow()
        for var in list(range(len(window))):
            if len(data) < var+1:
                break
            parsedPacket = packet.parse(data[var])
            if parsedPacket[0] == '3' and len(data) == 1:
                EOT(data[var])
            else:
                sendPacket = data[l].encode()
                transmitterSocket.sendto(sendPacket,emulatorAddress)
                print("sent"+data[l]+"\n")
                transmitterLog.write("sent"+data[l]+"\n")
                l = l + 1
        l = 0

        #listening for acks
        for var in list(range(len(window))):
            transmitterSocket.settimeout(TIMEOUT/1000)
            recvdata = transmitterSocket.recv(1024)
            packetString = recvdata.decode()
            pac = packet.parse(packetString)
            pac = list(pac)
            print("recieved"+packetString+"\n")
            transmitterLog.write("recieved"+packetString+"\n")
            if pac[0] == '3':
                print("Transmission confiremed complete")
                transmitterLog.close()
                exit()
            moveWindow(pac)
    except socket.timeout:
        print("Timeout error")
        continue

transmitterLog.close()
print('finished')
exit()
