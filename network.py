#! python3
import socket
import threading
import hashlib
import time
import datetime
import random
from packet import packet

def connections(address, instruction):
    drop_count=0
    packet_count=0

address = "localhost" #debug
networkPort = 8000
# Start - Connection initiation
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (address, networkPort)
sock.bind(server_address)

#while True:
#    print('Waiting to receive message')
#    instruction, address = sock.recvfrom(1024)
#    connectionThread = threading.Thread(target=connections, args=(address, instruction))
#    connectionThread.start()

while True:
    transmitterIP = input("Enter transmitter IP>")
    recieverIP = input("Enter reciever IP>")