import os
import sys
sys.path.append('../')

from time import sleep
### Minient-wifi Dependencies
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import UserAP, RemoteController
### SDS Dependencies
from Components.SDS_eNodeB import SD_eNodeB
from Components.SDS_C_Car import SD_C_Car
from Components.SDS_Car import SD_Car
from Components.SDS_Station import SDStorage_Station
from Components.SDS_Car_Switch import SD_Car_Switch
from Components.SDS_VANET_Controller import SDVanet_Controller
from Components.SDS_Station import SDStorage_Station


Car = SD_Car
C_Car = SD_C_Car
Switch = SD_Car_Switch
Station = SDStorage_Station
eNodeB = SD_eNodeB
VanetController = SDVanet_Controller

class InbandController(RemoteController):

    def checkListening(self):
        "Overridden to do nothing."
        return

def topology():
    print "Decentralized Software Defined Computing at the edge of the Network"
    print "--------------------------------------------------------------------"
    car_type = Car
    "Create a network"
    net = Mininet(controller=VanetController, link=TCLink, accessPoint=UserAP, switch=SD_Car_Switch, station=Station, enable_wmediumd=True, enable_interference=True)

    print "*** Creating Nodes ***"
    cars = []
    stas = []
    for x in range(0,10):
        cars.append(x)
        stas.append(x)
        cars[x] = net.addCar('car%s' % (x), wlans=1,
                             ip='10.0.0.%s/8' % (x + 1), cls=car_type)

    # adding eNodes
    e1 = net.addAccessPoint('e1', ssid='vanet-ssid', mac='00:00:00:11:00:01', mode='g', channel='1',
                            passwd='123456789a', encrypt='wpa2', position='3332.62,3253.92,0', cls=eNodeB)
    e2 = net.addAccessPoint('e2', ssid='vanet-ssid', mac='00:00:00:11:00:02', mode='g', channel='1',
                            passwd='123456789a', encrypt='wpa2', position='3279.02,3736.27,0', cls=eNodeB)
    e3 = net.addAccessPoint('e3', ssid='vanet-ssid', mac='00:00:00:11:00:03', mode='g', channel='11',
                            passwd='123456789a', encrypt='wpa2', position='2806.42,3395.22,0', cls=eNodeB)
    e4 = net.addAccessPoint('e4', ssid='vanet-ssid', mac='00:00:00:11:00:04', mode='g', channel='6',
                            passwd='123456789a', encrypt='wpa2', position='2320.82,3565.75,0', cls=eNodeB)
    e5 = net.addAccessPoint('e5', ssid='vanet-ssid', mac='00:00:00:11:00:05', mode='g', channel='6',
                            passwd='123456789a', encrypt='wpa2', position='2887.62,2935.61,0', cls=eNodeB)
    e6 = net.addAccessPoint('e6', ssid='vanet-ssid', mac='00:00:00:11:00:06', mode='g', channel='11',
                            passwd='123456789a', encrypt='wpa2', position='2351.68,3083.40,0', cls=eNodeB)

    client = net.addHost('cloud', cls=Cloud_host)
    switch = net.addSwitch('switch', dpid='4000000000000000', cls=SD_Switch)
    c1 = net.addController(
        'c1', controller=Vanet_controller, ip='127.0.0.1', port=6653)
    net.propagationModel("logDistancePropagationLossModel", exp=2.8)

if __name__ == '__main__':
    setLogLevel('debug')
    topology()
