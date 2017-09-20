#!/usr/bin/python
import sys
from mininet.node import OVSSwitch,UserSwitch, Host, Controller, RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.util import custom

import time


class SDStorage_Controller( Controller ):
      "Controller to run a SDStorage functions."

      def __init__( self, name,custom_type="storage_controller", **kwargs ):
          Controller.__init__( self, name,**kwargs )
          self.custom_type=custom_type


      def Initialize_resources(self,net):
          #HostID=1
          host_num_files=20
          host_num_dir=10
          host_size=5
          host_used=0
          """MEC STUFF"""
          basestation_num_files=100
          basestation_num_dir=50
          basestation_size=25
          basestation_used=0
          """AR STUFF"""
          AR_Library=[]
          #[content_identifier,content_name,content_size]
          AR_content=[1,"CityAR.fbx",5000]
          AR_Library.append(AR_content)
          AR_content=[2,"CarAR.obj",2000]
          AR_Library.append(AR_content)
          AR_content=[3,"StreetAR.fbx",1000]
          AR_Library.append(AR_content)
          AR_content=[4,"HeritageAR.jpg",850]
          AR_Library.append(AR_content)
          #nodes= net.hosts + net.stations
          """for host in net.hosts:
              host.NO_of_Dir=host_num_dir
              host.NO_of_files=host_num_files
              host.file_size=host_size
              host.Used_space=host_used
              msg=[]
              msg.append(host.IP())
              Fun1=self.get_capacity(host,host.type)
              msg.append(Fun1)
              Fun2=self.isFull(host,host.type)
              msg.append(Fun2)
              Fun3=self.getNumOfFiles(host,host.type)
              msg.append(Fun3)
              Fun4=self.Available_space(host,host.type)
              msg.append(Fun4)
              msg.append(host.type)
              self.sendMsg_toSwitch("Add",msg,net)"""
          for station in net.stations:
              station.NO_of_Dir=host_num_dir
              station.NO_of_files=host_num_files
              station.file_size=host_size
              station.Used_space=host_used
              msg=[]
              msg.append(station.IP())
              cap=self.get_capacity(station,station.type)
              msg.append(cap)
              isfull=self.isFull(station,station.type)
              msg.append(isfull)
              files=self.getNumOfFiles(station,station.type)
              msg.append(files)
              av_space=self.Available_space(station,station.type)
              msg.append(av_space)
              msg.append(station.type)
              #send message to access point
              self.send_msg_to_accesspoint("Add",station,msg,net)
          count=0
          for accessPoint in net.accessPoints:
              accessPoint.NO_of_Dir=basestation_num_dir
              accessPoint.NO_of_files=basestation_num_files
              accessPoint.file_size=basestation_size
              accessPoint.used_space=basestation_used
              msg=[]
              msg.append(accessPoint.params['mac'])
              cap=self.get_capacity(accessPoint,accessPoint.type)
              msg.append(cap)
              isfull=self.isFull(accessPoint,accessPoint.type)
              msg.append(isfull)
              files=self.getNumOfFiles(accessPoint,accessPoint.type)
              msg.append(files)
              av_space=self.Available_space(accessPoint,accessPoint.type)
              msg.append(av_space)
              msg.append(accessPoint.type)
              #Localizing AR contnet for each accesspoint
              msg.append(AR_Library[count])
              count+=1
              #new item
              self.send_msg_to_accesspoint("mec",accessPoint,msg,net)

      def Handle_switch_packets(self,status,Used_space,HostID,net):
          " Get a message from the switch and handle it."
          if status == "Add":
             network=self.addDir(net)
             return network
          elif status == "Update":
               self.update_Switch_FT(Used_space,HostID,net)

      def Handle_AP_message(self,operation,data,sta_IP,mac_id,net):
          " Get a message from the access point and handle it"
          if (operation == "Add"):
              network=self.addDir(net)
              return network
          elif (operation == "Update"):
              self.update_AccessPoint_FT(data,sta_IP,net)
          elif (operation == "mec_Update"):
              self.update_AccessPoint_Mec(data,mac_id,net)
          elif (operation == "AR"):
              res=self.search_AR_MEC(data,mac_id,net)
              return res



      def sendMsg_toSwitch(self,status,message,Topo):
          " Send a message to the switch to notify it with any change "
          msg=message
          Topo.switches[0].Handle_controller_packets(status,msg)
      def send_msg_to_accesspoint(self,operation,node,FT,net):
          "send a message to the access point to notify the changes "
          if(node.type == 'accessPoint'):
              node.Handle_controller_FT_update(operation,FT)
          else:
              #node is station
              ap=node.params['associatedTo'][0]
              #print ("node type is %s associated to %s type"%(node.type,ap.type))
              ap.Handle_controller_FT_update(operation,FT)

      def update_Switch_FT(self, Used_space,HostID,net):
          " Update the Functions valus in case a new store happend "
          for host in net.hosts:
              if host.IP()==HostID:
                 #print host.Used_space ,host.NO_of_Dir ,host.NO_of_files,host.file_size , host.name
                 host.Used_space+=Used_space
                 msg=[]
                 msg.append(host.IP())

                 Fun1=self.get_capacity(host,host.type)
                 #print host.Used_space ,host.NO_of_Dir ,host.NO_of_files,host.file_size, host.name
                 msg.append(Fun1)
                 Fun2=self.isFull(host,host.type)
                 msg.append(Fun2)
                 Fun3=self.getNumOfFiles(host,host.type)
                 msg.append(Fun3)
                 Fun4=self.Available_space(host,host.type)
                 msg.append(Fun4)

                 self.sendMsg_toSwitch("Update",msg,net)
                 #print "Why"
                 break

      def update_AccessPoint_FT(self,used_space,sta_IP,net):
          "update stations parameters in case any new data is stored"
          for station in net.stations:
              if (station.IP() == sta_IP):
                  station.Used_space+=used_space
                  msg=[]
                  msg.append(station.IP())
                  cap=self.get_capacity(station,station.type)
                  msg.append(cap)
                  isfull=self.isFull(station,station.type)
                  msg.append(isfull)
                  files=self.getNumOfFiles(station,station.type)
                  msg.append(files)
                  av_space=self.Available_space(station,station.type)
                  msg.append(av_space)
                  #send message to access point
                  self.send_msg_to_accesspoint("Update",station,msg,net)

      def search_AR_MEC(self,data,mac_id,net):
          found=False
          #print ("controller received AR request for id:%s"%data)
          for ap in net.accessPoints:
              if(ap.params['mac'] == mac_id):
                  continue
              else:
                  #search AP for requested AR content
                  for AR_content in ap.AR_Library:
                      for i in range(len(AR_content)):
                          if(i == 0):
                              #print ("AR identifier inside AP is %s holding %s and passed identifier is %s "%(AR_content[0],AR_content[1],content_identifier))
                              if(AR_content[i] == data):
                                  #print "AR content found"
                                  found = True
                                  #print("AR content found in AP[%s]"%(ap.params['mac']))
                                  #sleep thread to memic search time in another MEC

                                  #Consider file size when applying latency
                                  sleep_time=(AR_content[i+2]/1000)*0.0000018
                                  #Consider num of hubs when applying latency
                                  sleep_time+=0.03
                                  time.sleep(sleep_time)
                                  #print ("result in controller: %s"%found)
                                  return found
                              else:
                                  time.sleep(0.03)

                          else:
                              break
          if(not found):
              time.sleep(0.1)
              #print ("can not find the requested AR content within all accesspoints")
              return False



      def update_AccessPoint_Mec(self,used_space,mac_id,net):
          #print ("controller->Update MEC[%s] storage with %s datasize",used_space)
          for ap in net.accessPoints:
              if (ap.params['mac'] == mac_id):
                  ap.Used_space+=used_space
                  msg=[]
                  msg.append(ap.params['mac'])
                  cap=self.get_capacity(ap,ap.type)
                  msg.append(cap)
                  isfull=self.isFull(ap,ap.type)
                  msg.append(isfull)
                  files=self.getNumOfFiles(ap,ap.type)
                  msg.append(files)
                  av_space=self.Available_space(ap,ap.type)
                  msg.append(av_space)
                  msg.append(ap.type)
                  self.send_msg_to_accesspoint("mec_Update",ap,msg,net)
                  break

      def addDir(self,net):
          " Add a Dir to the Storage_Host."
          #TODO: check if node type (this metho were handling hosts only, and has been changed to stations)
          for station in net.stations:
              station.NO_of_Dir+=1
              msg=[]
              #msg.append(HostID)
              msg.append(station.IP())
              Fun1=self.get_capacity(station,station.type)
              msg.append(Fun1)
              Fun2=self.isFull(station,station.type)
              msg.append(Fun2)
              Fun3=self.getNumOfFiles(station,station.type)
              msg.append(Fun3)
              Fun4=self.Available_space(station,station.type)
              msg.append(Fun4)
              self.send_msg_to_accesspoint("Update",station,msg,net)
          return net

      def get_capacity(self,node,node_type):
          if(node_type == "host"):
              Cap= (node.NO_of_Dir*node.NO_of_files*node.file_size)
          elif(node_type == "station"):
              Cap= (node.NO_of_Dir*node.NO_of_files*node.file_size)
          elif(node_type == "accessPoint"):
              Cap= (node.NO_of_Dir*node.NO_of_files*node.file_size)
          return Cap

      def isFull(self,node,node_type): #Fun2
          "Check if the storage host is full or not!"
          if (node_type == "host"):
              if self.get_capacity(node,node_type)== node.Used_space:
                 return "Yes"
              else:
                 return "No"
          elif (node_type == "station"):
              if self.get_capacity(node,node_type)== node.Used_space:
                 return "Yes"
              else:
                 return "No"
          elif (node_type == "accessPoint"):
              if self.get_capacity(node,node_type)== node.Used_space:
                 return "Yes"
              else:
                 return "No"



      def getNumOfFiles(self,node,node_type): #Fun3
          "Return the total number of the files on the host storage"
          return node.NO_of_Dir*node.NO_of_files

      def Available_space(self,node,node_type): #Fun4
          "return total_space-used_space"
          res=self.get_capacity(node,node_type)- node.Used_space
          return res


	 #def Used_space(self, NO_of_Dir,NO_of_files,file_size)
         #for Dir in Dirs
           	#	for file in files
                 #   if file is not """
