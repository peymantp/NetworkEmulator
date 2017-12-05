#! python3
import hashlib
class packet:
    '''
    This module keeps track of the packets sent for one transmission

    packetType type:int,
        0 = Data,
        1 = ACK,
        3 = EOT
    '''
    delim = "|:|"

    def __init__(self,packetType, SeqNum, WindowSize, AckNum, Data=""):
        self.packetType = packetType
        self.seqNum     = SeqNum
        self.windowSize = WindowSize
        self.ackNum     = AckNum
        self.data = Data #TODO implement sha1

    def toString(self):
        stringPacket = (str(self.packetType) +packet.delim
                        +str(self.seqNum)    +packet.delim
                        +str(self.windowSize)+packet.delim
                        +str(self.ackNum)
                        #+packet.delim+self.data
                        )
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
        packetArray = str(p).split(packet.delim)
        return packetArray
