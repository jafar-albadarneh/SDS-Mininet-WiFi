#!/usr/bin/pyhton

import os
from mininet.node import Car
import time


class SD_C_Car(Car):
    "Storage Station is a host that operates with a wireless interface card"

    def __init__(self, name, custom_type="sd_car", NO_of_Dir=0, NO_of_files=0, file_size=0, Used_space=0, **pars):
        Car.__init__(self, name, **pars)
        self.NO_of_files = NO_of_files
        self.NO_of_Dir = NO_of_Dir
        self.file_size = file_size
        self.Used_space = Used_space
        self.custom_type = custom_type

        # TODO: Caching contents should be dynamic
        """Cached AR Content"""
        self.AR_Library = []
        # [content_identifier,content_name,content_size]
        AR_content = [1, "CityAR.fbx", 5000]
        self.AR_Library.append(AR_content)
        AR_content = [2, "CarAR.obj", 9000]
        self.AR_Library.append(AR_content)
        AR_content = [3, "StreetAR.fbx", 3000]
        self.AR_Library.append(AR_content)
        AR_content = [4, "HeritageAR.jpg", 850]
        self.AR_Library.append(AR_content)
        AR_content = [5, "MallAR.fbx", 5000]
        self.AR_Library.append(AR_content)
        AR_content = [6, "statueAR.obj", 9000]
        self.AR_Library.append(AR_content)
        AR_content = [7, "StAR.fbx", 3000]
        self.AR_Library.append(AR_content)
        AR_content = [8, "HallAR.jpg", 850]
        self.AR_Library.append(AR_content)
        """AR_content = [9, "shopAR.fbx", 3500]
        self.AR_Library.append(AR_content)
        AR_content = [10, "DinasorAR.obj", 8650]
        self.AR_Library.append(AR_content)"""


    def RequestContent(self, net, op=1):
        print ("\nAR content \t|\t Time \t\t|   Status")
        print ("-----------\t|\t ----------\t| ----------")
        for i in range(1, 11):
            start3 = time.time()
            if (self.foundIncache(i)):
                result = "Found/cache"
            else:
                result = self.escalateRequest(i, "mec", net, op)
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


    def getAssociatedAp(self):
        result = self.cmd('iw dev car2-wlan0 scan')
        res2 = result.split()[1]
        res2 = res2.split('(')[0]
        return (res2)

    def escalateRequest(self, content_identifier, mode, net, op):
        if (mode == "mec"):
            """getting accessPoint the station is associated to"""
            ap = self.params['associatedTo'][0]
            success = False

            index = 0
            for accessPoint in net.accessPoints:
                if (op == 1):
                    if (accessPoint.params['mac'] == ap.params['mac']):
                        result = net.accessPoints[index].Handle_Content_Request(content_identifier, net)
                        break
                    else:
                        index += 1
                else:  # v2v
                    if ("00:00:00:11:00:05" in accessPoint.params[
                        'mac']):  # TODO: fetch associated MEC dynamically when bgscan-enabled
                        result = net.accessPoints[index].Handle_Content_Request(content_identifier, net)
                        break
                    else:
                        index += 1

            return result


        else:
            """SD Search"""

    def foundIncache(self, content_identifier):
        found = False
        for AR_content in self.AR_Library:
            #print ("the content is: %s " % AR_content[1])
            if (AR_content[0] == content_identifier):
                sleep_time = (AR_content[2] / 1000) * 0.0000018
                time.sleep(sleep_time)
                found = True
            else:
                # cache search peneality in the same car
                time.sleep(0.0001)
                pass

            if (found):
                break
        return found