#!/usr/bin/pyhton

class latencyModel():
    """This should facilitate the latency cost of SD Network Operations"""
    @staticmethod
    def fileTransferLatency(size):
        # TODO: replace with a scientific real equation
        return (size/1000)*0.0000018
    @staticmethod
    def nextHopLatency():
        # latency per Hub jump
        return 0.03
    @staticmethod
    def searchPenality():
        """search peneality in the same MEC node"""
        return 0.0001




