class packet:
    def __init__(self, packetType : int, seqNum : int, windowSize : int, ackNum: int):
        self.packetType = packetType
        self.seqNum     = seqNum
        self.windowSize = windowSize
        self.ackNum     = ackNum
    