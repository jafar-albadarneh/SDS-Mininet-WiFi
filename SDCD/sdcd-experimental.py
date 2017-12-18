#!/usr/bin/python

import os
import sys
sys.path.append('../')

from time import sleep

from Components.SDS_C_Car import SD_C_Car
from Components.SDS_Car import SD_Car
# SDS Dependencies
from Components.SDS_Car_Switch import SD_Car_Switch
from Components.SDS_Host import Cloud_Host
from Components.SDS_Station import SDStorage_Station
from Components.SDS_VANET_Controller import SDVanet_Controller
from Components.SDS_eNodeB import SD_eNodeB
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import UserAP, RemoteController

from Components.SDS_Switch import SDStor_Switch

Vanet_controller = SDVanet_Controller
SD_Switch = SDStor_Switch
SD_station = SDStorage_Station
eNodeB = SD_eNodeB
Cloud_host = Cloud_Host


class InbandController(RemoteController):

    def checkListening(self):
        "Overridden to do nothing."
        return


def topology():
    car_type = SD_Car
    op = raw_input("Choose Type of Experiment: (1)v2i \t (2)v2v \nChoice:")
    if(op == "1"):
        v2v = False
        pass
    else:
        v2v = True
        caching = raw_input(
            "What do you prefere to run:\n (1)car-level caching enabled (2)car-level caching disbled \nChoice: ")
        if(caching == "1"):
            car_type = SD_C_Car
        else:
            car_type = SD_Car

    "Create a network."
    net = Mininet(controller=Vanet_controller, accessPoint=UserAP,
                  switch=SD_Car_Switch, station=SD_station, enable_wmediumd=True, enable_interference=True)

    print "*** Creating nodes"
    cars = []
    stas = []
    for x in range(0, 10):
        cars.append(x)
        stas.append(x)
    for x in range(0, 10):
        cars[x] = net.addCar('car%s' % (x), wlans=1,
                             ip='10.0.0.%s/8' % (x + 1), encrypt='wpa2', cls=car_type)

    e1 = net.addAccessPoint('e1', wlans=2, ssid='vanet-ssid', mac='00:00:00:11:00:01', mode='g', channel='1',
                            passwd='123456789a', encrypt='wpa2', position='3332.62,3253.92,0', cls=eNodeB)
    e2 = net.addAccessPoint('e2', wlans=2, ssid='vanet-ssid', mac='00:00:00:11:00:02', mode='g', channel='1',
                            passwd='123456789a', encrypt='wpa2', position='3279.02,3736.27,0', cls=eNodeB)
    e3 = net.addAccessPoint('e3', wlans=2, ssid='vanet-ssid', mac='00:00:00:11:00:03', mode='g', channel='11',
                            passwd='123456789a', encrypt='wpa2', position='2806.42,3395.22,0', cls=eNodeB)
    e4 = net.addAccessPoint('e4', wlans=2, ssid='vanet-ssid', mac='00:00:00:11:00:04', mode='g', channel='6',
                            passwd='123456789a', encrypt='wpa2', position='2320.82,3565.75,0', cls=eNodeB)
    e5 = net.addAccessPoint('e5', wlans=2, ssid='vanet-ssid', mac='00:00:00:11:00:05', mode='g', channel='6',
                            passwd='123456789a', encrypt='wpa2', position='2887.62,2935.61,0', cls=eNodeB)
    e6 = net.addAccessPoint('e6', wlans=2, ssid='vanet-ssid', mac='00:00:00:11:00:06', mode='g', channel='11',
                            passwd='123456789a', encrypt='wpa2', position='2351.68,3083.40,0', cls=eNodeB)

    client = net.addHost('cloud', cls=Cloud_host)
    switch = net.addSwitch('switch', dpid='4000000000000000', cls=SD_Switch)
    c1 = net.addController(
        'c1', controller=Vanet_controller, ip='127.0.0.1', port=6653)
    net.propagationModel("logDistancePropagationLossModel", exp=2.8)

    if(v2v):
        print "*** Setting bgscan"
        net.setBgscan(signal=-45, s_inverval=5, l_interval=10)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    net.addLink(switch, e1)
    net.addLink(client, switch)
    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    net.addLink(e4, e5)
    net.addLink(e5, e6)

    """net.addMesh(e1, intf = 'e1-wlan1', ssid='mesh-ssid')
    net.addMesh(e2, intf = 'e2-wlan1', ssid='mesh-ssid')
    net.addMesh(e3, intf = 'e3-wlan1', ssid='mesh-ssid')
    net.addMesh(e4, intf = 'e4-wlan1', ssid='mesh-ssid')
    net.addMesh(e5, intf = 'e5-wlan1', ssid='mesh-ssid')
    net.addMesh(e6, intf = 'e6-wlan1', ssid='mesh-ssid')"""

    "Available Options: sumo, sumo-gui"
    net.useExternalProgram('sumo-gui', config_file='map.sumocfg')

    print "*** Starting network"
    net.build()
    c1.start()
    e1.start([c1])
    e2.start([c1])
    e3.start([c1])
    e4.start([c1])
    e5.start([c1])
    e6.start([c1])

    i = 201
    for sw in net.carsSW:
        sw.start([c1])
        os.system('ifconfig %s 10.0.0.%s' % (sw, i))
        i += 1

    i = 1
    j = 2
    for car in cars:
        car.cmd('ifconfig %s-wlan0 192.168.0.%s/24 up' % (car, i))
        car.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (car, i))
        car.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2

    i = 1
    j = 2
    for v in net.carsSTA:
        v.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (v, j))
        v.cmd('ifconfig %s-mp0 10.0.0.%s/24 up' % (v, i))
        v.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        i += 1
        j += 2

    for v1 in net.carsSTA:
        i = 1
        j = 1
        for v2 in net.carsSTA:
            if v1 != v2:
                v1.cmd('route add -host 192.168.1.%s gw 10.0.0.%s' % (j, i))
            i += 1
            j += 2

    # Assigning IPs for Access points wlan interfaces
    IPs = ['90','91','92','93','94','95','96']
    for i in range(0,6):
        net.accessPoints[i].cmd('ifconfig e%s-wlan1 192.168.0.%s'%(i+1,IPs[i]))
        net.accessPoints[i].extIP = '192.168.0.%s'%(IPs[i])

    c1.initializeNetworkResources(net)

    if(v2v):
        raw_input("Press Enter to continue (wait 30sec after t=28)...")
        os.system('clear')
        os.system('ovs-ofctl mod-flows car2SW in_port=2,actions=drop')
        cars[2].cmdPrint('iwconfig car2-wlan0')
        sleep(3)
        cars[6].cmdPrint('iwconfig car6-wlan0')
        print "****************************************************"
        print "*** Both car2 and car6 are associated to enodeB5 ***"
        print "****************************************************"
        sleep(6)
        os.system('clear')
        print "****************************************************************"
        print "*** Car6 is so far from enodeB5. Trying to send data by car2 ***"
        print "****************************************************************"
        sleep(6)
        os.system('clear')
        print "**************************************"
        print "*** Trying to send data to car6... ***"
        print "**************************************"
        cars[2].cmdPrint('ping -c5 10.0.0.7')
        print "****************************************************************************************************"
        print "*** Car2: V2V is blocked! Car6 is unreachable! Controller, please let me talk directly with car6 ***"
        print "****************************************************************************************************"
        sleep(6)
        os.system('clear')
        print "***********************************************"
        print "*** controller says: Car6 is now reachable! ***"
        print "***********************************************"
        os.system('ovs-ofctl mod-flows car2SW in_port=2,actions=1')
        sleep(6)
        os.system('clear')
        cars[2].cmdPrint('ping -c5 10.0.0.7')
        os.system('clear')
        print "***********************************"
        print "*** Car2: Requesting Content for car6! ***"
        print "***********************************"
        sleep(1)
        cars[2].RequestContent(net, 2)
        print "***********************************"
        print "*** Car2: Thank you Controller! ***"
        print "***********************************"
    else:
        print "***********************************"
        print "********  V2I experiment **********"
        print "***********************************"
        raw_input("PressEnter after T=28 ...")

        print "type>> py car4.RequestContent(net)"

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
