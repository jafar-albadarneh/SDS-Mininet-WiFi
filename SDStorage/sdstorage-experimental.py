#!/usr/bin/python

"""
   Veicular Ad Hoc Networks - VANETs

"""
import os
import sys

from mininet.wifi.net import Mininet_wifi
from mininet.wifi.link import wmediumd
sys.path.append('../')
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import random
import time
from Components.SDS_RSU import SD_RSU
from Components.SDS_VANET_Controller import SDVanet_Controller
from Components.SDS_Switch import SDStor_Switch
from Components.SDS_Car import SD_Car
from Components.SDS_Station import SDStorage_Station
from Components.config import Modes
import pdb

RSU = SD_RSU
VANET_Controller = SDVanet_Controller
SD_Switch = SDStor_Switch
SD_station = SDStorage_Station

def topology():

    "Create a network."
    net = Mininet_wifi(controller=VANET_Controller, link=wmediumd,
                  switch=SD_Switch, station=SD_station, enable_interference=True)

    print ("*** Creating nodes")
    car = []
    stas = []
    mec = []
    channel = ['1','6','11']
    NUM_OF_MECS = 4
    for x in range(0, 5):
        car.append(x)
        stas.append(x)
    for x in range(0, 5):
        min = random.randint(1,10)
        max= random.randint(11,30)
        car[x] = net.addCar('car%s' % (x+1), wlans=1, ip='10.0.0.%s/8' % (x + 1), min_speed=min, max_speed=max,cls=SD_Car)

    c = 0
    for m in range(0, NUM_OF_MECS):
        mec.append(m)
    for m in range(0,NUM_OF_MECS):
        #print "Counter of mecs is %s "%m
        if((m+1) % 3 == 0):
            c=0
        mec[m] = net.addAccessPoint('MEC%s' % (m+1), ssid= 'RSU%s' % (m+1), mode= 'g', channel= channel[c], range=100 ,cls=RSU)
        c += 1

    c1 = net.addController( 'c1', controller=VANET_Controller )


    def SDStorage(datasize):
        start2 = time.time()
        datasize = int(datasize)
        print ("car %s want to store %s bytes" % (0, datasize))
        car[0].store(datasize,Modes.MEC, net)
        end2 = time.time()
        with open('Storage.txt', 'a') as f:
            f.write('%.12f \n' % (end2-start2))
        print ("took : ", end2 - start2)

    print ("*** Configuring wifi nodes")
    net.configureWifiNodes()

    #net.meshRouting('custom')

    print ("*** Associating and Creating links")
    for m in range(0, NUM_OF_MECS):
        if(m < (NUM_OF_MECS-1)):
            net.addLink(mec[m],mec[m+1])
        else:
            net.addLink(mec[0],mec[m])


    """uncomment to plot graph"""
    net.plotGraph(max_x=700, max_y=700)

    """Number of Roads"""
    net.roads(10)

    """Start Mobility"""
    net.startMobility(time=0)

    print ("*** Starting network")
    net.build()
    c1.start()

    c1.initializeNetworkResources(net)
    print ("Draw 10 roads and place the 4 MEC nodes along them?")
    print ("\n\n\n***************************START*******************************")
    datasize = raw_input("What is the amount of storage you want (in bytes)")
    SDStorage(datasize)
    print ("\n\n\n***************************END*******************************")
    print ("(MEC) info Table after the test")
    net.aps[0].listMecContents(Modes.MEC, net)
    print ("*** Running CLI")
    CLI( net )

    print ("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
