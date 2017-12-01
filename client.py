#! python3
import socket
import os
from os import path
from packet import packet
import sys
import argparse

#Create help
parser=argparse.ArgumentParser(
    description='''Client app can be set as reciever or transmitter in the network. ''')
parser.add_argument('mode', type=int,help='0=reciever or 1=transmitter')
parser.add_argument('-server', dest="server", default="localhost", help='IP address of the network emulator')
args = parser.parse_args()
if args.mode != 0 or args.mode != 1:
    print("Invalid argument " + str(args.mode) + " for mode. please try again")
    sys.exit()
#print settings
print(args._get_args)

#currentAddress = socket.gethostbyname(socket.getfqdn()) #selects first non localhost in etc/hosts
serverAddress = args.server
msgPort = 8000
msgSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dataPort = 7000
dataSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
