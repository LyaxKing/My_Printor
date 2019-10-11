# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:57:51 2019

@author: HP
"""
import serial
import re
import os
import json


class print_state:
    alive = 0
    printing = 0
    endprint = 0
    startprint = 0
    process = 0
    chambertemperature = 0
    bedtemperature = 0
    timeout = 0.5

    def __init__(self, printid, portname, baudrate, sio, tem_position):
        self.portname = portname
        self.baudrate = baudrate
        self.printid = printid
        self.sio = sio
        self.tem_position = tem_position
        self.ser = serial.Serial(self.portname, self.baudrate, timeout=self.timeout)

    def start(self):
        # 判断串口是否已经打开
        if self.ser.isOpen():
            self.alive = 1
            return True
        else:
            return False

    def tem_get(self):
        print('get tem')
        tem = []
        tem_order = "M105\n".encode('ascii')
        self.ser.write(tem_order)
        while True:
            read_order = self.ser.readline()
            #self.ser.flushOutput()
            if ("ok" in bytes.decode(read_order) or "done" in bytes.decode(read_order)):
                tem = re.findall(r"\d+\.?\d*", bytes.decode(read_order))
                if len(tem) == None:
                    tem = [0, 0, 0, 0]
                self.chambertemperature = tem[self.tem_position[0]]
                self.bedtemperature = tem[self.tem_position[1]]
                break

    def get_statue_json(self):
        statue_json = {
            'id': self.printid,
            'on_off': self.alive,
            'status': {
                'chambertemperature': self.chambertemperature,
                'bedtemperature': self.bedtemperature
            },
            'printing': self.printing,
            'endprint': self.endprint,
            'startprint': self.startprint,
            'process': self.process
        }
        return statue_json

    def read_gcode(self):
        # 读取gcode文件，读到list
        filename = "printfile.gcode"
        gcodelist = []
        with open(filename, 'r') as gcodefile:
            temp_gcodelist = gcodefile.readlines()
        for line in temp_gcodelist:
            if not line.startswith(';'):
                gcodelist.append(line)
        return gcodelist

    def print_model(self, gcodelist):
        i = 0
        j = len(gcodelist)
        for line in gcodelist:
            self.process = i / j
            line = str.encode(line)
            if line == ";End of Gcode":
                self.printing = 0
                self.endprint = 1
                break
            else:
                self.printing = 1
            self.ser.write(line)
            while True:
                read_order = self.ser.readline()
                if ("ok" in bytes.decode(read_order) or "done" in bytes.decode(read_order)):
                    if i % 10 == 0:
                        self.tem_get()
                        statue_json = self.get_statue_json()
                        self.sio.emit('status', statue_json)
                        print(statue_json)
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    i = i + 1
                    break
        self.sio.emit('status', statue_json)
        self.endprint = 0
        print("打印结束,，发送打印机状态：")
        print(statue_json)
        os.remove("printfile.gcode")
        self.process = 0


def read_port_information():
    fp = open("portinfor.json", 'wr')
    port_infor = json.load(fp)
    tem_position = []
    if len(fp) == 0:
        printid = input("Enter your printid: ")
        portname = input("Enter your portname: ")
        baudrate = input("Enter your baudrate: ")
        tem_position.append(input("Enter your tem_position1: "))
        tem_position.append(input("Enter your tem_position2: "))
        printor_json = {
            'printid': printid,
            'portname': portname,
            'baudrate': baudrate,
            'tem_position': tem_position
        }
        json.dump(printor_json, fp)
    else:
        portname = port_infor['portname']
        baudrate = port_infor['baudrate']
        printid = port_infor['printid']
        tem_position = port_infor['tem_position']
    return portname, baudrate, printid, tem_position


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)
