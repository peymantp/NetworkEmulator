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
emulatorSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
emulatorSocket.bind(emulatorAddress)
#log file
time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
transmitterLog = open("transmitterLog"+time+".md",'x')

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
    for var in list(range(PACKETLIMIT-1)):
        pac = packet(0, var, WINDOWSIZE, var)
        packetstring = pac.toString()
        data.append(packetstring)
    pac = packet(3, var, WINDOWSIZE, var)
    packetstring = pac.toString()
    print(packetstring+"\n") #debug line
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
    emulatorSocket.send(_sendPacket)
    #log packet sent
	transmitterLog.write("sent"+data+"\n")

def moveWindow(pac):
    for var in range(data.__len__):
        if(str(data[var].seqNum) == pac[1]):
            del data[var]

packetCreation()
l=0
while not data: #send while data is not empty
    try:
        prepWindow()
        for var in list(range(len(window))):
            if data[var].packetType == 3 and data.__len__ == 1:
                EOT(data[var])
            else:
                sendPacket = data[l].encode()
                emulatorSocket.send(sendPacket)
                #log packet sent
				transmitterLog.write("sent"+data+"\n")
                l = l + 1
        l = 0
        emulatorSocket.settimeout(TIMEOUT)

        #listening for acks
        for var in list(range(len(window))):
            data, addr = emulatorSocket.recv()
            packetString = data.decode()
            pac = packet.parse(packetString)
            #packet recieved
			transmitterLog.write("recieved"+data+"\n")
            if pac[0] == 3:
                print("Transmission confiremed complete")
            moveWindow(pac)

    except socket.timeout as TIMEOUTERROR:
        print(TIMEOUTERROR)
        print("Exiting program")
        break


transmitterLog.close()
print('finished')
exit()
