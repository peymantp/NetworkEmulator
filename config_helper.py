class ConfigHelper:
    '''
    For reading IP and port numbers of reciever, transmitter and Network Emulator
    IP should be written as
        ip=0.0.0.0
    Ports should be written as
        port=XXXX
    '''
    def __init__(self,path):
        configFile = open(path,'r')
        global configFileLines
        configFileLines = configFile.readlines()
    
    def getEmulartor(path):
        """ getting a tuple (ip,port) of the Network Emulator"""
        #Emulator IP should be in line 2
        emulatorIP = configFileLines[1].replace('\n','').split('=')[1]
        #Emulator IP should be in line 3
        emulatorPort = configFileLines[2].replace('\n','').split('=')[1]
        return (emulatorIP,emulatorPort)

    def getTransmitter(path):
        """ getting a tuple (ip,port) of the Transmitter"""
        #Transmitter IP should be in line 6
        transmitterIP = configFileLines[5].replace('\n','').split('=')[1]
        #Transmitter IP should be in line 7
        transmitterPort = configFileLines[6].replace('\n','').split('=')[1]
        return (transmitterIP,transmitterPort)

    def getReciever(path):
        """ getting a tuple (ip,port) of the Reciever"""
        #Reciever IP should be in line 9
        recieverIP = configFileLines[8].replace('\n','').split('=')[1]
        #Reciever IP should be in line 10
        recieverPort = configFileLines[9].replace('\n','').split('=')[1]
        return (recieverIP,recieverPort)
