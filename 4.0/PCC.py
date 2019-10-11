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
        self.print_file_alive = 0

    def printor_alive(self):
        # 判断串口是否已经打开
        if self.ser.isOpen():
            self.alive = 1
            return True
        else:
            return False

    def tem_get(self):
        tem_order = "M105\n".encode('ascii')
        self.ser.write(tem_order)
        while True:
            read_order = self.ser.readline()
            self.ser.flushOutput()
            if ("ok" in bytes.decode(read_order) or "done" in bytes.decode(read_order)):
                tem = re.findall(r"\d+\.?\d*", bytes.decode(read_order))
                if tem == None:
                    tem = [0, 0, 0, 0]
                try:
                    self.chambertemperature = tem[self.tem_position[0]]
                    self.bedtemperature = tem[self.tem_position[1]]
                except:
                    break
                print(tem)
                break

    def get_statue_json(self):
        statue_json = {
            'id': self.printid,
            'on_off': self.alive,
            'chambertemperature': self.chambertemperature,
            'bedtemperature': self.bedtemperature,
            'printing': self.printing,
            'process': self.process
        }
        return statue_json

    def print_model(self, filename="printfile.gcode"):
        gcodelist = []
        with open(filename, 'r') as gcodefile:
            temp_gcodelist = gcodefile.readlines()
        for line in temp_gcodelist:
            if not line.startswith(';'):
                gcodelist.append(line)
        i = 0
        j = len(gcodelist)
        self.printing = 1
        for line in gcodelist:
            self.process = i / j * 100
            print(self.process)
            line = str.encode(line)
            if line == ";End of Gcode":
                self.printing = 0
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
        if filename == "printfile.gcode":
            os.remove("printfile.gcode")
        print("打印结束")
        self.process = 0
        self.print_file_alive = 0

    def pause_printor(self):
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
