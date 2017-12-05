#! python3
from packet import packet
import socket
from time import sleep
from config_helper import ConfigHelper as conf

config = conf("config")
recieverAddress = config.getReciever()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost',9999))

pac = packet(0, 0, 0, 0)
pac1 = packet(0, 1, 0, 1)
pac2 = packet(0, 2, 0, 2)
pac3 = packet(0, 3, 0, 3)
pac4 = packet(0, 3, 0, 3)
pac5 = packet(0, 3, 0, 3)
pac6 = packet(3, 4, 0, 4)

s.sendto(pac.toString().encode(), recieverAddress)
sleep(0.05)
s.sendto(pac1.toString().encode(),recieverAddress)
sleep(0.05)
s.sendto(pac2.toString().encode(),recieverAddress)
sleep(0.05)
s.sendto(pac3.toString().encode(),recieverAddress)
sleep(0.05)
s.sendto(pac4.toString().encode(),recieverAddress)
sleep(0.05)
s.sendto(pac5.toString().encode(),recieverAddress)
sleep(0.05)
s.sendto(pac6.toString().encode(),recieverAddress)
sleep(0.05)