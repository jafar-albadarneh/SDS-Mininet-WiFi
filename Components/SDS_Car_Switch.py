#!/usr/bin/python

import sys
from mininet.node import OVSKernelSwitch
from operator import itemgetter
from config import Type,Operations,Modes


# guppy: actual memory consumption


class SD_Car_Switch(OVSKernelSwitch):
    "Switch to connect different types of storage hosts like StorageHost"

    def __init__(self, name, custom_type=Type.SD_CAR_SWITCH, **pars):
        OVSKernelSwitch.__init__(self, name, **pars)
        print ("custom swtich has been initialized")
        self.Function_table = []
        self.counter = 0
        self.custom_type = custom_type
        self.MEC = []
        """AR Content"""
        self.AR_Library = []

    def update_AR(self, msg):
        self.MEC = []
        for attrib in range(len(msg) - 1):
            self.MEC.append(msg[attrib])
        self.AR_Library.append(msg[len(msg) - 1])

    def Handle_controller_packets(self, operation, message):
        packetstatus = operation
        SDSObject = message
        if (packetstatus == Operations.CONTENT_DELIVERY):
            self.update_AR(SDSObject)

    def sendMsg_toCon(self, status, Used_space, HostID, net):
        " Send a message to the controller to notify it with any change"
        if status == "Add":
            network = net.controllers[0].Handle_switch_packets(
                "Add", None, None, net)
            return network
        elif status == "Update":
            net.controllers[0].Handle_switch_packets(
                "Update", Used_space, HostID, net)

    def print_switch_info(self, mode, net):
        if (mode == Modes.CONTENT_DELIVERY):
            print (
                "[MAC Address]\t{AR Library} \n ***************************")
            for sw in net.switches:
                if (sw.custom_type != "sd_car_switch"):
                    continue
                print ("%s \t " % sw.MEC[0])
                count = 0
                for AR in sw.AR_Library:
                    for i in range(len(AR)):
                        print ("content: %s" % (AR[i]))
                    count += 1
                    print ("------")
