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

#log file
time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
recieverLog = open("recieverLog"+time+".md",'x')

receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiveSocket.bind(transmitterAddress)

WINDOWSIZE = 5
RETRANSMIT = 200
TIMEOUT = 2000
BYTESREAD = 1024
windowIndex = 0
seqNumArray = []
ackNumArray = []
data = []
seq = 0
ack = 0
EOT = False

#read file being sent and store inside window #
filename = 'test.txt'
with open(filename, 'r') as f:
    while True:
        buffer = f.read(BYTESREAD)
        if not buffer: break
        data.append()


#https://stackoverflow.com/a/6822907
def window(seq,size=WINDOWSIZE):
    """
    for each in window(range(6), 3):
        print(list(each))
[0, 1, 2]\n
[1, 2, 3]\n
[2, 3, 4]\n
[3, 4, 5]\n
    """
    iters = tee(seq, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each, None)
    return izip(*iters)

while not EOT:
    #SOT packet
    pac = packet(2, seq, WINDOWSIZE, 0, filename)
    packetstring = pac.toString()
    #https://www.youtube.com/watch?v=lk27yiITOvU
    


recieverLog.close()
print('finished')
exit()
