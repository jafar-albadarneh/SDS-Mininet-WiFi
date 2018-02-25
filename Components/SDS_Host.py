#!/usr/bin/python

import os
from mininet.node import Host
#from FunctionTable import *
from Components.contentLibrary import contentLibrary
from .config import Type

class Cloud_Host(Host):

    "Host Storage where other hosts can store the data inside it "

    def __init__(self, name, custom_type=Type.SD_CLOUD_HOST, NO_of_Dir=10, NO_of_files=20, file_size=5, Used_space=0, **pars):
        Host.__init__(self, name, **pars)
        self.NO_of_files = NO_of_files
        self.NO_of_Dir = NO_of_Dir
        self.file_size = file_size
        self.Used_space = Used_space
        self.custom_type = custom_type
        """AR Content"""
        self.cLibrary = contentLibrary()

        print ("Cloud host has been initialized")
