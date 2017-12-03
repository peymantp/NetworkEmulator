#! python3
import hashlib
class packet:
    '''
    This module keeps track of the packets sent for one transmission

    packetType type:int,
        0 = Data,
        1 = ACK,
        2 = SOT,
        3 = EOT
    '''
    delim = "|:|"
    packetType = 0
    seqNum = 0
    windowSize = 0
    ackNum = 0
    data = ""
    def create(packetType, SeqNum, WindowSize, AckNum, Data=""):
        packetType = packetType
        seqNum     = SeqNum
        windowSize = WindowSize
        ackNum     = AckNum
        data = Data #TODO implement sha1

    def toString():
        stringPacket = (str(packet.packetType) +packet.delim
                        +str(packet.seqNum)    +packet.delim
                        +str(packet.windowSize)+packet.delim
                        +str(packet.ackNum)    +packet.delim
                        +packet.data)
        return stringPacket
    
    @staticmethod
    def parse(p):
        '''
        array[0] = Packet type\n
        array[1] = sequence number\n
        array[2] = Window size\n
        array[3] = ack number\n
        array[4] = data (if data packet)
        '''
        packetArray = p.split(packet.delim)
        return packetArray
