#!/usr/bin/pyhton

class ITG():
    """ D-ITG traffic configurations """
    protocol = 'UDP' # -T
    generationDuration = 100 # in milliseconds -t
    numOfKilobytes = 1024 # -r
    numOfPackets = None # -z
    # when -z,-t,-k selected, the most constructive will be applied
    packetSize = 10 # -c
    senderLogFile = 'sender.log'
    receiverLogFile = 'receiver.log'

    @staticmethod
    def getMecMeshIP(self, mec):
        """ responsible for getting the IP attached to the MEC "wlan1" interface
            to facilitate passing traffic among connected vehicles """
        return mec.getMeshIP()

    @staticmethod
    def getMecExternalIP(self, mec):
        """ responsible for getting the IP attached to the MEC mesh "mp2" interface
            to facilitate passing traffic among neighboring mec nodes"""
        return mec.getExternalIP()

    @staticmethod
    def getVehicleExternalIP(car):
        """ responsible for getting the IP attached to the car "wlan0" interface
            in order to pass traffic to cars through mec nodes' "wlan1" interfaces"""
        # bash>> 'ifconfig %s | grep -Eo "([0-9]{1,3}\.){3}[0-9]{1,3}" | head -1'
        return car.getExternalIP()

    @staticmethod
    def sendTraffic(source , destination, dataSize = numOfKilobytes):
        """ responsible for sending traffic from a source to a destination """
        """ activate ITG-Reciever Listener inside destination MEC node """
        destination.cmd("ITGRecv &")
        destinationIP = None
        if(isinstance(destination, UserAP)):
            destinationIP = ITG.getMecMeshIP(destination)
        elif(isinstance(destination, Car)):
            destinationIP = ITG.getVehicleExternalIP(destination)

        """ Send Traffic among neighboring MEC nodes """
        protocol = ITG.protocol # -T
        generationDuration = ITG.generationDuration # -t
        numOfkilobytes = dataSize # -k
        numOfPackets = None # -z
        """ when -z,-t,-k selected, the most constructive will be applied """
        packetSize = 10 # -c
        senderLogFile = '%s-%s'%(source.name, ITG.senderLogFile)
        receiverLogFile = '%s-%s'%(destination.name, ITG.receiverLogFile)

        if(destinationIP != None):
            source.cmdPrint("sudo ITGSend "
                 "-T %s " # protocol
                 "-a %s " # destination IP
                 "-k %s " # number of kilobytes
                 "-t %s " # generation duration 
                 "-l %s " # sender log
                 "-x %s" # receiver log
                 %(protocol,destinationIP,numOfkilobytes,generationDuration,senderLogFile,receiverLogFile))
