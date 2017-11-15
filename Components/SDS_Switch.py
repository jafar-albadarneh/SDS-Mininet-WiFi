#!/usr/bin/python

from operator import itemgetter

from mininet.node import OVSKernelSwitch
from config import Modes, Operations, Type


# guppy: actual memory consumption

class SDStor_Switch(OVSKernelSwitch):
    "Switch to connect different types of storage hosts like StorageHost"

    def __init__(self, name, custom_type=Type.SD_SWITCH, **pars):
        OVSKernelSwitch.__init__(self, name, **pars)
        print ("custom swtich has been initialized")
        self.Function_table = []
        self.counter = 0
        self.custom_type = custom_type
        self.MEC = []
        """Content"""
        self.cLibrary = []

    def insert_entry(self, SDSObject):
        self.Function_table.append([])
        for index in range(len(SDSObject)):
            self.Function_table[self.counter].append(SDSObject[index])

        L = sorted(self.Function_table, key=itemgetter(4), reverse=True)
        self.Function_table = L
        self.counter += 1

    def update_AR(self, msg):
        self.MEC = []
        for attrib in range(len(msg) - 1):
            self.MEC.append(msg[attrib])
            # print ("attrib %s -> %s"%(attrib,self.MEC[attrib]))
        self.cLibrary.append(msg[len(msg) - 1])

    def update_entry(self, SDSObject):
        HostIP = SDSObject[0]
        index = 0
        # print len(self.Function_table)
        while (index < len(self.Function_table)):

            if (HostIP == self.Function_table[index][0]):
                self.Function_table[index][1] = SDSObject[1]
                self.Function_table[index][2] = SDSObject[2]
                self.Function_table[index][3] = SDSObject[3]
                self.Function_table[index][4] = SDSObject[4]

                # L=sorted(self.Function_table,key=itemgetter(4),reverse=True)
                # self.Function_table=L

                # print self.Function_table
                break
            index += 1

    def remove_entry(self, SDSObject):
        HostIP = SDSObject[0]
        index = 0
        while index < len(self.Function_table):
            if (HostIP == self.Function_table[index][0]):
                self.Function_table.pop(index)
                break
        sorted(self.Function_table, key=itemgetter(4))

    def Handle_controller_packets(self, operation, message):
        " Get a message from the controller and handle it."
        packetstatus = operation
        SDSObject = message

        if packetstatus == "Add":
            self.insert_entry(SDSObject)
        elif packetstatus == "Update":
            self.update_entry(SDSObject)
        elif (packetstatus == Operations.CONTENT_DELIVERY):
            self.update_AR(SDSObject)
        else:
            self.remove_entry(SDSObject)

    def sendMsg_toCon(self, status, Used_space, HostID, net):
        " Send a message to the controller to notify it with any change"
        if status == "Add":
            network = net.controllers[0].Handle_switch_packets(
                "Add", None, None, net)
            return network
        elif status == "Update":
            net.controllers[0].Handle_switch_packets(
                "Update", Used_space, HostID, net)

    def sendMesg_toHost(message):
        pass
        # send a message to the host

    def store_data(data):
        pass
        # Store the data on the underling storage hosts.
