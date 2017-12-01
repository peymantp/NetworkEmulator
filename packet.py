#! python3
import hashlib
class packet:
    def __init__(self, packetType, seqNum, windowSize, ackNum, data=""):
        self.packetType = packetType
        self.seqNum     = seqNum
        self.windowSize = windowSize
        self.ackNum     = ackNum
        checksum = data #TODO implement sha1
