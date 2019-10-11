# -*- coding: utf-8 -*-
from socket import *
import json
host ='47.96.95.75'
#host = '192.168.1.110'
port = 10000
bufsize = 1024*1024
addr = (host, port)
class StatueReportor:
    def __init__(self):
        self.udptcpCliSock = socket(AF_INET, SOCK_DGRAM)

    def senddata(self, data):
        data = bytes(json.dumps(data), encoding='utf-8')
        self.udptcpCliSock.sendto(data, addr)

