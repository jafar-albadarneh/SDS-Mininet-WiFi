#!/usr/bin/python
import sys
from mininet.node import OVSSwitch,UserSwitch, Host, Controller, RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.util import custom

import time


class SDVanet_Controller( Controller ):
      "Controller to run a SDStorage functions."

      def __init__( self, name,custom_type="vanet_controller", **kwargs ):
          Controller.__init__( self, name,**kwargs )
          self.custom_type=custom_type
          self.RSUs=[]
          self.eNodeBs=[]


      def Initialize_resources(self,net):
          AR_Library=[]
          #[content_identifier,content_name,content_size]
          AR_content = [1, "CityAR.fbx", 5000]
          AR_Library.append(AR_content)
          AR_content = [2, "CarAR.obj", 9000]
          AR_Library.append(AR_content)
          AR_content = [3, "StreetAR.fbx", 3000]
          AR_Library.append(AR_content)
          AR_content = [4, "HeritageAR.jpg", 850]
          AR_Library.append(AR_content)
          AR_content = [5, "MallAR.fbx", 5000]
          AR_Library.append(AR_content)
          AR_content = [6, "statueAR.obj", 9000]
          AR_Library.append(AR_content)
          AR_content = [7, "StAR.fbx", 3000]
          AR_Library.append(AR_content)
          AR_content = [8, "HallAR.jpg", 850]
          AR_Library.append(AR_content)
          AR_content = [9, "shopAR.fbx", 3500]
          AR_Library.append(AR_content)
          AR_content = [10, "DinasorAR.obj", 8650]
          AR_Library.append(AR_content)
          for host in net.hosts:
              if(host.custom_type == "sd_cloudHost"):
                  msg=[]
                  msg.append(host.IP())
                  msg.append(host.type)
                  self.sendMsg_toSwitch("Add",host,msg,net)
              else:
                  continue
          for switch in net.switches:
              if(switch.custom_type == "sd_switch"):
                  msg = []
                  msg.append("'[02:00:00:00:0k:00]'")
                  msg.append(switch.type)
                  AR_content = []
                  for i in range(0,10):
                      AR_content.append(AR_Library[i])

                  msg.append(AR_content)
                  self.sendMsg_toSwitch("AR", switch, msg, net)

              else:
                  continue
          for car in net.cars:
              msg=[]
              msg.append(car.IP())
              msg.append(car.type)

          count=0
          for accessPoint in net.accessPoints:
              if(accessPoint.custom_type == "sd_eNodeB"):
                  self.eNodeBs.append(accessPoint)
              elif(accessPoint.custom_type == "sd_switch"):
                  continue
              msg=[]
              msg.append(accessPoint.type)
              AR_content=[]
              AR_content.append(AR_Library[count])
              count+=1
              msg.append(AR_content)
              self.send_msg_to_accesspoint("mec",accessPoint,msg,net)

      def Handle_switch_packets(self,status,Used_space,HostID,net):
          if status == "Update":
               self.update_Switch_FT(Used_space,HostID,net)

      def Handle_AP_message(self,operation,data,sta_IP,mac_id,net):
          if (operation == "Update"):
              self.update_AccessPoint_FT(data,sta_IP,net)
          if (operation == "AR"):
              res=self.search_MEC(data, mac_id, net)
              return res



      def sendMsg_toSwitch(self,operation,node,FT,net):
          if(node.type == "switch"):
            node.Handle_controller_packets(operation,FT)

      def send_msg_to_accesspoint(self,operation,node,FT,net):
          if(node.type == 'accessPoint'):
              node.Handle_controller_FT_update(operation,FT)
          elif(node.type == "vehicle"):
              #node is car
              ap=node.params['associatedTo'][0]
              ap.Handle_controller_FT_update(operation,FT)
          else:
              ap= node.params['associatedTo'][0]
              ap.Handle_controller_FT_update(operation,FT)
              #node is station

      def update_Switch_FT(self, Used_space,HostID,net):
          for host in net.hosts:
              if host.IP()==HostID:
                 host.Used_space+=Used_space
                 msg=[]
                 msg.append(host.IP())
                 self.sendMsg_toSwitch("Update",msg,net)
                 break

      def update_AccessPoint_FT(self,used_space,sta_IP,net):
          "update stations parameters in case any new data is stored"
          for station in net.stations:
              if (station.IP() == sta_IP):
                  station.Used_space+=used_space
                  msg=[]
                  msg.append(station.IP())
                  #send message to access point
                  self.send_msg_to_accesspoint("Update",station,msg,net)

      def search_MEC(self, data, mac_id, net):
          found=False
          THRESHOLD = 4
          counter = 1
          for ap in net.accessPoints:
              if (counter >= THRESHOLD):
                  break
              if(ap.params['mac'] == mac_id):
                  continue
              else:
                  for AR_content in ap.AR_Library:
                      for c in AR_content:
                          for i in range(len(c)):
                              if(i == 0):
                                  if(c[i] == data):
                                      found = True
                                      #sleep thread to memic search time in another MEC

                                      #Consider file size when applying latency
                                      sleep_time=(c[i+2]/1000)*0.0000018
                                      #Consider num of hubs when applying latency
                                      sleep_time+=0.03
                                      time.sleep(sleep_time)
                                      return found
                                  else:
                                      # search peneality in the same MEC node
                                      time.sleep(0.0001)

                              else:
                                  break
                  time.sleep(0.03)
                  #print ("counter: %s"%counter)
                  counter = counter +1

          if(not found):
              for sw in net.switches:
                  if(sw.custom_type == "sd_switch"):
                      for AR_content in sw.AR_Library:
                          for c in AR_content:
                              for i in range(len(c)):
                                  if(i == 0):
                                      if (c[i] == data):
                                          found=True
                                          sleep_time = (c[i + 2] / 1000) * 0.0000018
                                          # Consider num of hubs when applying latency
                                          sleep_time += 0.06
                                          time.sleep(sleep_time)
                                          return found
                                      else:
                                          time.sleep(0.0001)

                  else:
                      #not switch, might be (AP,MEC,eNodeB)
                      continue

              return found
