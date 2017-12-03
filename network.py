#! python3
import socket
import threading
import hashlib
import time
import datetime
import random
from packet import packet
import argparse
from config_helper import ConfigHelper as conf

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

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(emulatorAddress)

def transmitter(data):
    return

def reciever(data):
    return

print("server emulator running")
while True:
    data, addr = s.recvfrom()
    print("Comparing %s to transmitter %s" % (addr,transmitterAddress)
    if addr == transmitterAddress:
        transmitter(data)
    print("Comparing %s to reciever %s" % (addr,recieverAddress))
    if addr == recieverAddress:
        transmitter(data)
