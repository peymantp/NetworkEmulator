#! python3
import argparse
import datetime
import hashlib
import random
import socket
import threading
import time

from config_helper import ConfigHelper as conf
from packet import packet

#Program argument initilisation
parser=argparse.ArgumentParser(
    description='Network emulator for testing how diffrent protocols will behave with varing BER and packet delays.')
parser.add_argument('BER', type=int, default=0, help='Bit Error Rate 0-100')
parser.add_argument('packetDelay', type=int, default=0, help='Packet delay in milliseconds')
args = parser.parse_args()
# Error checking for program arguments
if args.BER > 100 or args.BER < 0:
    print("BER must be within 0 and 100")
if args.packetDelay < 0:
    print("Packer delay must be a positive number")

#reading from config file
config = conf("config")
emulatorAddress = config.getEmulartor()
recieverAddress = config.getReciever()
transmitterAddress = config.getTransmitter()

packetsRecieved = 0
packetsDropped = 0
packetsSent = 0
currentBER = 0
EOF = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(emulatorAddress)

def drop():
    """
    Drop packets if random generated number is equal or smaller than BER
    Unless the current BER is higher than requested which means the program doesn't intentionnaly drop the packet
    """
    drop = False
    currentBER = packetsDropped/packetsRecieved*100 #percentage of packets dropped
    if currentBER >= args.BER:
        return drop
    ran = random.randint(1,101)
    if ran < args.BER:
        drop = True
    return drop    

def transmitter(data):
    time.sleep(args.packetDelay)
    s.sendto(data,recieverAddress)
    return

def reciever(data):
    time.sleep(args.packetDelay)
    s.sendto(data,transmitterAddress)
    packetArray = packet.parse(data)
    if packetArray[0] == 3:
       EOF = True
    return

print("server emulator running")
while not EOF:
    data, addr = s.recv()
    packetsRecieved += 1
    if drop():
        packetsDropped += 1
    else:    
        print("Comparing %s to transmitter %s" % (addr,transmitterAddress))
        if addr[0] == transmitterAddress[0] and addr[1] == transmitterAddress[1]:
            transmitter(data)
            print("Comparing %s to reciever %s" % (addr,recieverAddress))
        elif addr[0] == recieverAddress[0] and addr[1] == recieverAddress[1]:
            transmitter(data)

print("Packets recieved: " + packetsRecieved + "\n"
    "Packets sent " + packetsSent + "\n"
    "Packets droped " + packetsDropped)
