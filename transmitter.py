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
    for var in range(data.__len__):
        if(str(data[var].seqNum) == pac[1]):
            del data[var]

packetCreation()
l=0
while len(data) > 0: #send while data is not empty
    try:
        prepWindow()
        for var in list(range(len(window))):
            parsedPacket = packet.parse(data[var])
            if parsedPacket[0] == '3' and data.__len__ == 1:
                EOT(data[var])
            else:
                sendPacket = data[l].encode()
                transmitterSocket.sendto(sendPacket,emulatorAddress)
                print("sent"+sendPacket+"\n")
                transmitterLog.write("sent"+sendPacket+"\n")
                l = l + 1
        l = 0
        transmitterSocket.settimeout(TIMEOUT)

        #listening for acks
        for var in list(range(len(window))):
            data = transmitterSocket.recv(1024)
            packetString = data.decode()
            pac = packet.parse(packetString)
            pac = list(pac)
            print("recieved"+data+"\n")
            transmitterLog.write("recieved"+data+"\n")
            if pac[0] == '3':
                print("Transmission confiremed complete")
            moveWindow(pac)
    except socket.timeout:
        print("Timeout error")
        print("Exiting program")
        break


transmitterLog.close()
print('finished')
exit()
