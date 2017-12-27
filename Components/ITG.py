#!/usr/bin/pyhton
import os

import shutil
from mininet.node import UserAP, Car
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
    def getMecMeshIP(mec):
        """ responsible for getting the IP attached to the MEC "wlan1" interface
            to facilitate passing traffic among connected vehicles """
        return mec.getMeshIP()

    @staticmethod
    def getMecExternalIP(mec):
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
    def sendTraffic(source, destination, content):
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
        numOfkilobytes = content[2] # -k
        numOfPackets = None # -z
        """ when -z,-t,-k selected, the most constructive will be applied """
        packetSize = 10 # -c
        senderLogFile = 'c%s/%s-%s-%s'%(content[0],source.name, content[0], ITG.senderLogFile)
        receiverLogFile = 'c%s/%s-%s-%s'%(content[0],destination.name,content[0], ITG.receiverLogFile)

        # create the directory if does not exists
        directory = 'c%s'%content[0]
        if not os.path.exists(directory):
            os.makedirs(directory)

        if(destinationIP != None):
            source.cmdPrint("sudo ITGSend "
                 "-T %s " # protocol
                 "-a %s " # destination IP
                 "-k %s " # number of kilobytes
                 "-t %s " # generation duration 
                 "-l %s " # sender log
                 "-x %s" # receiver log
                 %(protocol,destinationIP,numOfkilobytes,generationDuration,senderLogFile,receiverLogFile))

        # DELETE LOG FOLDERS AND CONTENTS
        # shutil.rmtree(directory, ignore_errors=False, onerror=None)
