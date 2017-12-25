#!/usr/bin/pyhton

import os
from mininet.node import Car
import time

from ITG import ITG
from config import Modes,Type
from latencyModel import latencyModel


class SD_C_Car(Car):
    "Storage Station is a host that operates with a wireless interface card"

    def __init__(self, name, custom_type=Type.SD_C_CAR, NO_of_Dir=0, NO_of_files=0, file_size=0, Used_space=0, **pars):
        Car.__init__(self, name, **pars)
        self.NO_of_files = NO_of_files
        self.NO_of_Dir = NO_of_Dir
        self.file_size = file_size
        self.Used_space = Used_space
        self.custom_type = custom_type

        # TODO: Caching contents should be dynamic
        """Cached AR Content"""
        self.cLibrary = []
        # [content_identifier,content_name,content_size]
        content = [1, "City.fbx", 5000]
        self.cLibrary.append(content)
        content = [2, "Car.obj", 9000]
        self.cLibrary.append(content)
        content = [3, "Street.fbx", 3000]
        self.cLibrary.append(content)
        content = [4, "Heritage.jpg", 850]
        self.cLibrary.append(content)
        content = [5, "Mall.fbx", 5000]
        self.cLibrary.append(content)
        content = [6, "statue.obj", 9000]
        self.cLibrary.append(content)
        content = [7, "Sta.fbx", 3000]
        self.cLibrary.append(content)
        content = [8, "Hall.jpg", 850]
        self.cLibrary.append(content)


    def RequestContent(self, net, op=1):
        print ("\nAR content \t|\t Time \t\t|   Status")
        print ("-----------\t|\t ----------\t| ----------")
        for i in range(1, 11):
            start3 = time.time()
            if (self.foundIncache(i)):
                result = "Found/cache"
            else:
                result = self.escalateRequest(i, Modes.MEC, net, op)
                if (result):
                    result = "Found"
                else:
                    result = "Not Found"

            if (op != 1):
                # TODO: this was added to emulate the latency for transfering the content to the other car
                time.sleep(0.03)
                end3 = time.time()
                with open('v2v.csv', 'a') as f:
                    f.write('%s,%.12f \n' % (i, end3 - start3))
            else:
                end3 = time.time()
                with open('v2i.csv', 'a') as f:
                    f.write('%s,%.12f \n' % (i, end3 - start3))

            print (" %s \t \t \t %.12f \t%s" % (i, end3 - start3, result))

    def getAssociatedAP(self):
        result = self.cmd('iw dev %s-wlan0 link'%self.name)
        if(result != 'Not Connected'):
            mac_address = result.split()[2]
            return mac_address
        else:
            raise ValueError("Vehicle is not connected")

    def getExternalIP(self):
        return self.externalIP

    def decodeRXResults(self):
        receiverLog = '%s-receiver.log'%self.name
        self.cmdPrint("ITGDec %s"%receiverLog)

    def sendTrafficToCar(self, car, dataSize):
        ITG.sendTraffic(self, car, dataSize)

    def escalateRequest(self, content_identifier, mode, net, op):
        if (mode == Modes.MEC):
            """getting accessPoint the station is associated to"""
            ap = self.params['associatedTo'][0]
            index = 0
            for accessPoint in net.aps:
                if (op == 1):
                    if (accessPoint.params['mac'] == ap.params['mac']):
                        result = net.aps[index].handleContentRequest(
                            content_identifier, net)
                        break
                    else:
                        index += 1
                else:  # v2v (bgscan enabled)
                    if (self.getAssociatedAP() in accessPoint.params[
                            'mac']):
                        result = net.aps[index].handleContentRequest(
                            content_identifier, net)
                        break
                    else:
                        index += 1

            return result

        else:
            """other modes"""

    def foundIncache(self, content_identifier):
        found = False
        for content in self.cLibrary:
            #print ("the content is: %s " % content[1])
            if (content[0] == content_identifier):
                sleep_time = latencyModel.fileTransferLatency(content[2])
                time.sleep(sleep_time)
                found = True
            else:
                # cache search peneality in the same car
                time.sleep(latencyModel.searchPenality())
                pass

            if (found):
                break
        return found
