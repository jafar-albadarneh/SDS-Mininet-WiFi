#!/usr/bin/python

import os
from mininet.node import Host
#from FunctionTable import *

class Cloud_Host(Host):

    "Host Storage where other hosts can store the data inside it "

    def __init__( self, name,custom_type="sd_cloudHost", NO_of_Dir=10,  NO_of_files=20,file_size=5,Used_space=0,**pars ):
        Host.__init__(self, name, **pars)
        self.NO_of_files=NO_of_files
        self.NO_of_Dir=NO_of_Dir
        self.file_size=file_size
        self.Used_space=Used_space
        self.custom_type=custom_type
        """AR Content"""
        self.AR_Library=[]
        #[content_identifier,content_name,content_size]
        AR_content=[1,"CityAR.fbx",5000]
        self.AR_Library.append(AR_content)
        AR_content=[2,"CarAR.obj",9000]
        self.AR_Library.append(AR_content)
        AR_content=[3,"StreetAR.fbx",3000]
        self.AR_Library.append(AR_content)
        AR_content=[4,"HeritageAR.jpg",850]
        self.AR_Library.append(AR_content)
        AR_content = [5, "MallAR.fbx", 5000]
        self.AR_Library.append(AR_content)
        AR_content = [6, "statueAR.obj", 9000]
        self.AR_Library.append(AR_content)
        AR_content = [7, "StAR.fbx", 3000]
        self.AR_Library.append(AR_content)
        AR_content = [8, "HallAR.jpg", 850]
        self.AR_Library.append(AR_content)
        AR_content = [9, "resturantAR.fbx", 3000]
        self.AR_Library.append(AR_content)
        AR_content = [10, "policeStationAR.fbx", 850]
        self.AR_Library.append(AR_content)

        """
        for AR in self.AR_Library:
            for i in range(len(AR)):
                print ("index %s: content: %s"%(i,AR[i]))
        """

        print "Cloud host has been initialized"
