#!/usr/bin/pyhton

import os
from mininet.node import Car
import time


class SD_Car(Car):
    "Storage Station is a host that operates with a wireless interface card"

    def __init__(self, name, custom_type="sd_car", NO_of_Dir=0, NO_of_files=0, file_size=0, Used_space=0, **pars):
        Car.__init__(self, name, **pars)
        self.NO_of_files = NO_of_files
        self.NO_of_Dir = NO_of_Dir
        self.file_size = file_size
        self.Used_space = Used_space
        self.custom_type = custom_type

    def RequestContent(self, net, op=1):
        print ("\nAR content \t|\t Time \t\t|   Status")
        print ("-----------\t|\t ----------\t| ----------")
        for i in range(1, 11):
            start3 = time.time()
            result = self.escalateRequest(i, "mec", net, op)
            if (result):
                result = "Found"
            else:
                result = "Not Found"

            if(op != 1):
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
            ap = self.params['associatedTo'][0]  # TODO:activate this for v2i experiment
            success = False

            index = 0
            for accessPoint in net.accessPoints:
                if(op == 1):
                    if (accessPoint.params['mac'] == ap.params['mac']):
                        result = net.accessPoints[index].Handle_Content_Request(
                            content_identifier, net)
                        break
                    else:
                        index += 1
                else:  # v2v
                    # TODO: fetch associated MEC with bgscan-enabled
                    if ("00:00:00:11:00:05" in accessPoint.params['mac']):
                        result = net.accessPoints[index].Handle_Content_Request(
                            content_identifier, net)
                        break
                    else:
                        index += 1

            return result

        else:
            """SD Search"""
    def store(self, datasize, mode, net):
        if (mode == "mec"):
            """MEC OPERATIONS"""
            # get the accessPoint the station is attached to
            for wlan in range(0, len(self.params['wlan'])):
                ap = self.params['associatedTo'][0]
                print ("Associated RSU is: %s with mac: %s" % (ap, ap.params['mac']))
                break
            index = 0
            # search if the accesspoint
            for accessPoint in net.accessPoints:
                if (accessPoint.custom_type == "sd_switch"):
                    continue
                if (accessPoint.params['mac'] == ap.params['mac']):
                    net.accessPoints[index].store_data(datasize, net)
                    print "an accessPoint found index %s" % index
                    break
                else:
                    index += 1
                # print "Total number of searched accessPoints are: %s"%(index+1)
        # TODO: add v2v storage mode