import sys
from mininet.node import OVSKernelSwitch,UserSwitch,OVSAP,OVSKernelAP, Host, Station, UserAP
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.util import custom
from array import *
from operator import itemgetter
from config import Modes, Operations,Type
import time
#TODO the implementation of this class should be identical from eNodeB class representing different functions.
class SD_RSU (UserAP):
    "custom AccessPoint to support SDSecure Storage"
    def __init__(self, name, custom_type=Type.SD_RSU, NO_of_Dir=100, NO_of_files=50, file_size=25, NO_of_RACKS=1, Used_space=0, **pars):
        UserAP.__init__(self, name, **pars)
#        OVSKernelAP.__init__(self, name, **pars)
        """MEC Attributes"""
        self.NO_of_Dir=NO_of_Dir
        self.NO_of_files=NO_of_files
        self.file_size=file_size
        self.Used_space=Used_space
        self.NO_of_RACKS=NO_of_RACKS
        self.custom_type=custom_type
        self.MEC=[]
        """"""

        """Contents"""
        self.cLibrary=[]

        """"""
        self.Function_table=[]
        self.counter=0

    def insert_entry(self,SDSObject):
        self.Function_table.append([]) #initialize the function table
        for index in range(len(SDSObject)):
            self.Function_table[self.counter].append(SDSObject[index])
        #sort the function table by the available space decending
        Sorted_FT=sorted(self.Function_table,key=itemgetter(4),reverse=True)
        self.Function_table=Sorted_FT
        self.counter+=1

    def update_entry(self,SDSObject):
        passed=False
        MEC_mac_address=SDSObject[0]
        if(MEC_mac_address == self.MEC[0]):
            passed=True
        if(passed):
            self.MEC = []
            print ("UpdatingMEC-> Allocating storage \n **************************")
            for attrib in range(len(SDSObject)):
                    self.MEC.append(SDSObject[attrib])
                    print ("attrib %s : %s"%(attrib,self.MEC[attrib]))


    def remove_entry(self, SDSObject):
        # get Station IP
        StationIP=SDSObject[0]
        index=0
        while( index < len(self.Function_table)):
            if(StationIP == self.Function_table[index][0]):
                self.Function_table.pop(index)
                break
            index+=1
        #resort AP-FT
        sorted(self.Function_table,itemgetter(4),reverse=True)

    def handleControllerUpdateRequest(self,operation, SDSObject):
        if(operation == 'Add'):
            self.insert_entry(SDSObject)
        elif(operation == 'Update'):
            self.update_entry(SDSObject)
        elif(operation == Operations.MEC):
            self.initializeMecContents(SDSObject)
        elif(operation == 'mec_Update'):
            self.update_mec(SDSObject)
        else:
            self.remove_entry(SDSObject)
    #this is temp should be removed
    def update_mec(self,msg):
        self.MEC=[]
        #print ("inside update_mec new available spce is%s"%msg[4])
        for attrib in range(len(msg)):
                self.MEC.append(msg[attrib])

    def initializeMecContents(self, msg):
        self.MEC=[]
        #print ("updating mec: adding attributes")
        #print ("********************************")
        for attrib in range(len(msg)-1):
            self.MEC.append(msg[attrib])
            #print ("attrib %s -> %s"%(attrib,self.MEC[attrib]))
        self.cLibrary.append(msg[len(msg) - 1])

    def listMecContents(self, mode, net):
        if(mode == Modes.MEC):
            print ("[MAC Address ,   Station Capacity ,     IsStationFull ,    Num of files ,     Available space]")
            for ap in net.aps:
                if(ap.custom_type == Type.SD_SWITCH):
                    continue
                #ap=self.MEC
                #print ("length of MEC is:%s"%len(ap))
                #print('[%s ,\t %s ,\t %s ,\t %s ,\t %s,\t %s,\t %s]' % (ap.MEC[0],ap.MEC[1],ap.MEC[2],ap.MEC[3],ap.MEC[4],ap.MEC[5],ap.AR_Library[0][1]))
                print('[%s ,\t %s ,\t %s ,\t %s ,\t %s,\t %s]' % (ap.MEC[0], ap.MEC[1], ap.MEC[2], ap.MEC[3], ap.MEC[4], ap.MEC[5]))
        elif(mode == Modes.CONTENT_DELIVERY):
            print ("[MAC Address]\t{AR Library} \n ***************************")
            for ap in net.aps:
                if (ap.custom_type == Type.SD_SWITCH):
                    continue
                print ("%s \t "%ap.MEC[0])
                count = 0
                for AR in ap.AR_Library:
                    for i in range(len(AR)):
                        print ("content: %s" % (AR[i]))
                    count += 1
                    print ("------")


        """
        count=0
        for AR in self.AR_Library:
            print "content %s"%count
            for i in range(len(AR)):
                print ("content: %s"%(AR[i]))
            count+=1
        """

    def Handle_controller_packets(self,status,message):
        " Get a message from the controller and handle it."
        packetstatus=status
        SDSObj= message

        if packetstatus == "Add":
           self.insert_entry(SDSObj)
        elif packetstatus =="Update":
             self.update_entry(SDSObj)
        else:
             self.remove_entry(SDSObj)

    def find_Node_with_available_space(self, datasize, net):
        found=False
        while(not found):
            for station_idx in range(len(self.Function_table)):
                Current_station=self.Function_table[station_idx]
                if (datasize == 0):
                    found=True
                    break
                else:
                    #data sent ain't empty
                    sta_available_space= Current_station[4]
                    sta_IP=Current_station[0]

                    if(datasize <= sta_available_space):
                        used_space=datasize
                        datasize=0 #the data have been stored successfully
                        found=True
                        #inform the controller
                        self.sendMsg_toCon("Update",used_space,sta_IP,None,net)
                    else:
                        #the file_size is larger than the Available_space
                        used_space=sta_available_space
                        datasize=datasize-used_space
                        #inform the controller
                        self.sendMsg_toCon("Update",used_space,sta_IP,None,net)

                    #if last station reached and the dataSize still large
                    #inform the controller to find space else where in another switch (if any left unchecked)
                    # in addition to inform the controller to activate new rackspaces in the stations
                    if (station_idx == (len(self.Function_table)-1) and datasize != 0):
                        self.sendMsg_toCon("Add",None,None,None,net)

    def sendMsg_toCon(self,operation,data,sta_IP,mac_id,net):
        if(operation == "Update"):
            net.controllers[0].Handle_AP_message("Update",data,sta_IP,None,net)
        elif (operation == "Add"):
            net.controllers[0].Handle_AP_message("Add",None,None,None,net)
        elif (operation == "mec_Update"):
            net.controllers[0].Handle_AP_message("mec_Update",data,None,mac_id,net)
        elif(operation == Operations.CONTENT_DELIVERY):
            res= net.controllers[0].Handle_AP_message(Operations.CONTENT_DELIVERY,data,None,mac_id,net)
            #print ("result in accesspoint(msg response): %s"%res)
            return res


    def send_msg_to_station(message):
        pass

    def Handle_AR_Content_Request(self,content_identifier,net):
        #print ("requested AR content has identifier %s"%content_identifier)
        #search current accessPoint
        index = 0
        found = False
        for AR_content in self.cLibrary:
            for c in AR_content:
                #print ("AR identifier inside AP is %s holding %s and passed identifier is %s "%(c[0],c[1],content_identifier))
                if(c[0] == content_identifier):
                    #print "AR content found locally"
                    #Consider file size when applying latency
                    sleep_time=(c[0+2]/1000)*0.0000018
                    time.sleep(sleep_time)
                    found = True
                else:
                    # search peneality in the same MEC node
                    time.sleep(0.0001)
                if(found):
                    break
        if(not found):
            #ask the controller to search another MEC node
            A_MEC_mac_address=self.MEC[0]
            res=self.sendMsg_toCon(Operations.CONTENT_DELIVERY,content_identifier,None,A_MEC_mac_address,net)
            #print ("result in accessPoint(CO MEC): %s"%res)
            return res
        #print ("result in accesspoint(Local MEC): %s"%found)
        return found


    def store_data(self,datasize,net):
        stored=False
        THRESHOLD = 4 #NUMBER OF MEC NODES TO BE SEARCHED
        sleep_time = 0
        while(not stored):
            if(datasize == 0):
                stored=True
                print ("data sent is empty")
                break
            else:
                #data is not empty
                A_MEC_available_space= self.MEC[4] #associated mec available space
                A_MEC_mac_address=self.MEC[0] #associate MEC macaddress in order to be sent to the controller to update it's vision about it
                if(datasize<= A_MEC_available_space):
                    print ("there is enough space for the data to be stored")
                    used_space=datasize
                    stored=True
                    #print ("AP-> tell the controller to save %s inside MEC"%used_space)
                    self.sendMsg_toCon("mec_Update",used_space,None,A_MEC_mac_address,net)

                    #simulate the delay of the store operation
                    sleep_time = (datasize/1000)*0.0000018
                    time.sleep(sleep_time)
                else:
                    #Seize the full amount of storage left inside the associated mec and
                    #let the controller find some other mec to save the rest
                    used_space=A_MEC_available_space
                    datasize=datasize-used_space
                    self.sendMsg_toCon("mec_Update",used_space,None,A_MEC_mac_address,net)
                    sleep_time = (datasize / 1000) * 0.0000018
                    time.sleep(sleep_time)
                    #the rest need to be stored on the next closest MEC
                    print ("only %s bytes has been stored, %s bytes need to be stored in another MEC node"%(used_space,datasize))
                    """Search AccessPoints in net"""
                    #TODO: this implementation assume that all accesspoints in the net, and should be moved to controller thou
                    # are connected to each others. it has to be optimized to consider only
                    # accesspoints that are linked to the associated MEC accesspoint
                    full=True
                    NUM_OF_APS=len(net.aps)
                    print ("Num of accesspoints is: %s"%NUM_OF_APS)
                    counter=0
                    for ap in net.aps:
                        print ("%s accesspoints have been searched" % counter)
                        if (counter == (NUM_OF_APS - 1) or (counter+1) >= THRESHOLD): #or (counter+1) >= THRESHOLD
                            print ("All APs are full and there is %s bytes left unstored" % used_space)
                            # Inform the controller to allocate storage inside accesspoints
                            ap.sendMsg_toCon("Add", None, None, None, net)
                            sleep_time = 0.05
                            time.sleep(sleep_time)

                        if(ap.params['mac'] == A_MEC_mac_address):
                            counter+=1
                            continue
                        else:
                            sleep_time=0.03; #added penality for MEC search
                            sleep_time = sleep_time + (counter)*0.1; #penality added for data transfer
                            time.sleep(sleep_time)
                            print("another accesspoint found inside net with mac address:%s"%ap.params['mac'])
                            ap_available_space=ap.MEC[4]
                            ap_mac_address=ap.params['mac']
                            #check if there is available space
                            if(datasize <= ap_available_space):
                                used_space=datasize
                                stored=True
                                print ("CO AP->tell the controller to save %s inside CO MEC %s"%(used_space,ap_mac_address))
                                ap.sendMsg_toCon("mec_Update",used_space,None,ap_mac_address,net)
                                #storage operation delay
                                sleep_time = sleep_time + (datasize / 1000) * 0.0000018
                                time.sleep(sleep_time)
                                stored = True
                                break #break the inner loop
                            else:
                                used_space=ap_available_space
                                datasize=datasize-used_space
                                ap.sendMsg_toCon("mec_Update",used_space,None,ap_mac_address,net)
                                counter+=1
                                #storage operation delay
                                sleep_time = sleep_time + (datasize / 1000) * 0.0000018
                                time.sleep(sleep_time)



    def printFT(self):
        print ("[IP Address ,   Station Capacity ,     IsStationFull ,    Num of files ,     Available space]")
        for index in range(len(self.Function_table)):
            station=self.Function_table[index]
            print('[%s ,\t %s ,\t %s ,\t %s ,\t %s]' % (station[0],station[1],station[2],station[3],station[4]))
