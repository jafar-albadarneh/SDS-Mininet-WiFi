import sys
from mininet.node import UserAP
from operator import itemgetter
import time
from config import Modes,Operations,Type


class SD_eNodeB (UserAP):
    "custom AccessPoint to support SDSecure Storage"

    def __init__(self, name, custom_type=Type.SD_E_NODEB, NO_of_Dir=100, NO_of_files=50, file_size=25, NO_of_RACKS=1, Used_space=0, **pars):
        UserAP.__init__(self, name, **pars)
        """MEC Attributes"""
        self.NO_of_Dir = NO_of_Dir
        self.NO_of_files = NO_of_files
        self.file_size = file_size
        self.Used_space = Used_space
        self.NO_of_RACKS = NO_of_RACKS
        self.custom_type = custom_type
        self.MEC = []
        """"""

        """ Content"""
        self.cLibrary = []

        """"""
        self.Function_table = []
        self.counter = 0

    def handleControllerUpdateRequest(self, operation, SDSObject):
        if(operation == Operations.MEC):
            self.initializeMecContents(SDSObject)

    def initializeMecContents(self, msg):
        self.MEC = []
        for attrib in range(len(msg) - 1):
            self.MEC.append(msg[attrib])
        self.cLibrary.append(msg[len(msg) - 1])

    def listMecContents(self, mode, net):
        if(mode == Modes.CONTENT_DELIVERY):
            print (
                "[MAC Address]\t{AR Library} \n ***************************")
            for ap in net.accessPoints:
                if (ap.custom_type == Type.SD_SWITCH):
                    continue
                print ("%s \t " % ap.MEC[0])
                count = 0
                for c in ap.cLibrary:
                    for i in range(len(c)):
                        print ("content: %s" % (c[i]))
                    count += 1
                    print ("------")

    def sendMsgToController(self, operation, data, sta_IP, mac_id, net):
        if(operation == Operations.CONTENT_DELIVERY):
            res = net.controllers[0].Handle_AP_message(
                Operations.CONTENT_DELIVERY, data, None, mac_id, net)
            return res

    def handleContentRequest(self, contentIdentifier, net):
        found = False
        for AR_content in self.cLibrary:
            for c in AR_content:
                for i in range(len(c)):
                    if(i == 0):
                        #print ("AR identifier inside AP is %s holding %s and passed identifier is %s "%(c[0],c[1],content_identifier))
                        if(c[i] == contentIdentifier):
                            # print "AR content found locally"
                            # Consider file size when applying latency
                            sleep_time = (c[i + 2] / 1000) * 0.0000018
                            time.sleep(sleep_time)
                            found = True
                        else:
                            # search peneality in the same MEC node
                            time.sleep(0.0001)

                    else:
                        break
                if(found):
                    break
        if(not found):
            # ask the controller to search another MEC node
            A_MEC_mac_address = self.MEC[0]
            res = self.sendMsgToController(
                Operations.CONTENT_DELIVERY, contentIdentifier, None, A_MEC_mac_address, net)
            #print ("result in accessPoint(CO MEC): %s"%res)
            return res
        #print ("result in accesspoint(Local MEC): %s"%found)
        return found
