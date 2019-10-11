# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:57:51 2019

@author: HP
"""
import serial
import re
import os



class PrintControl:
    alive = 0
    printing = 0
    endprint = 0
    startprint = 0
    process = 0
    chambertemperature = 0
    bedtemperature = 0
    timeout = 0.5

    def __init__(self, printid, portname, baudrate, tem_position):
        self.portname = portname
        self.baudrate = baudrate
        self.printid = printid
        self.tem_position = tem_position
        self.ser = serial.Serial(self.portname, self.baudrate, timeout=self.timeout)

    def is_start(self):
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
            self.ser.flushOutput()
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
            'chambertemperature': self.chambertemperature,
            'bedtemperature': self.bedtemperature,
            'printing': self.printing,
            'endprint': self.endprint,
            'startprint': self.startprint,
            'process': self.process
        }
        return statue_json

    def print_model(self):
        filename = "printfile.gcode"
        gcodelist = []
        with open(filename, 'r') as gcodefile:
            temp_gcodelist = gcodefile.readlines()
        for line in temp_gcodelist:
            if not line.startswith(';'):
                gcodelist.append(line)
        i = 0
        j = len(gcodelist)
        for line in gcodelist:
            self.process = i / j * 100
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
                    self.tem_get()
                    i = i + 1
                    break
        self.endprint = 0
        os.remove("printfile.gcode")
        self.process = 0

    def pause_print(self):
        print('Pausing>>>>>>>>>>>>>>>>>>')
        pause_order = "\n".encode('ascii')
        self.ser.write(pause_order)
        i = 0
        while i <= 500:
            read_order = self.ser.readline()
            self.ser.flushOutput()
            if ("ok" in bytes.decode(read_order) or "done" in bytes.decode(read_order)):
                return True
            i = i+1
        return False



