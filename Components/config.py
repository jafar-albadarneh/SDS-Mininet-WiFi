#!/usr/bin/pyhton

""" CUSTOM TYPES """
# Constants describing custom types
from mininet.node import UserAP, Car

class Type():
    """Constants describing custom types"""
    SD_CAR = "sd_car"
    SD_C_CAR = "sd_c_car"
    SD_CAR_SWITCH = "sd_car_switch"
    SD_SWITCH = "sd_switch"
    SD_E_NODEB = "sd_eNodeB"
    SD_CLOUD_HOST = "sd_cloudHost"
    SD_RSU = "sd_rsu"
    SD_STATION = "sd_station"
    SD_VANET_CONTROLLER = "vanet_controller"
    SD_STORAGE_CONTROLLER = "storage_controller"

    #MININET-WIFI Constants
    HOST = "host"
    STATION = "station"
    SWITCH = "switch"
    ACCESSPOINT = "ap"
    VEHICLE = "vehicle"


class Modes():
    """MODES of EXPERIMENTS """
    MEC = 1
    CONTENT_DELIVERY = 2

class Operations():
    """ OPERATION TYPES"""
    MEC = 1
    CONTENT_DELIVERY = 2
