import sys
from mininet.node import UserAP
from operator import itemgetter
import time


class SD_eNodeB (UserAP):
    "custom AccessPoint to support SDSecure Storage"

    def __init__(self, name, custom_type="sd_eNodeB", NO_of_Dir=100, NO_of_files=50, file_size=25, NO_of_RACKS=1, Used_space=0, **pars):
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

        """AR Content"""
        self.AR_Library = []

        """"""
        self.Function_table = []
        self.counter = 0

    def Handle_controller_FT_update(self, operation, SDSObject):
        if(operation == 'mec'):
            self.populate_mec(SDSObject)

    def populate_mec(self, msg):
        self.MEC = []
        for attrib in range(len(msg) - 1):
            self.MEC.append(msg[attrib])
        self.AR_Library.append(msg[len(msg) - 1])

    def print_mec_info(self, mode, net):
        if(mode == "AR"):
            print (
                "[MAC Address]\t{AR Library} \n ***************************")
            for ap in net.accessPoints:
                if (ap.custom_type == "sd_switch"):
                    continue
                print ("%s \t " % ap.MEC[0])
                count = 0
                for AR in ap.AR_Library:
                    for i in range(len(AR)):
                        print ("content: %s" % (AR[i]))
                    count += 1
                    print ("------")

    def sendMsg_toCon(self, operation, data, sta_IP, mac_id, net):
        if(operation == "AR"):
            res = net.controllers[0].Handle_AP_message(
                "AR", data, None, mac_id, net)
            return res

    def Handle_Content_Request(self, content_identifier, net):
        index = 0
        found = False
        for AR_content in self.AR_Library:
            for c in AR_content:
                for i in range(len(c)):
                    if(i == 0):
                        #print ("AR identifier inside AP is %s holding %s and passed identifier is %s "%(c[0],c[1],content_identifier))
                        if(c[i] == content_identifier):
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
            # print "not found Local MEC node"

            # ask the controller to search another MEC node
            A_MEC_mac_address = self.MEC[0]
            res = self.sendMsg_toCon(
                "AR", content_identifier, None, A_MEC_mac_address, net)
            #print ("result in accessPoint(CO MEC): %s"%res)
            return res
        #print ("result in accesspoint(Local MEC): %s"%found)
        return found
