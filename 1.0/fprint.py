
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 17:24:00 2019

@author: HP
"""

import socketio
import serial
import time
import re 
import os

class print_state:
    printing = 0
    endprint =0 
    startprint = 0
        
sio = socketio.Client()
serial = serial.Serial('/dev/ttyUSB0', 250000, timeout=0.5)
ps = print_state()
print("正在连接服务器")

def read_gcode(filename):
    #读取gcode文件，读到list
    gcodelist=[]
    with open(filename,'r') as gcodefile:
        temp_gcodelist = gcodefile.readlines()
    for line in temp_gcodelist:
        if line.startswith(";") or "\n" == line:
            continue
        gcodelist.append(line)
    return gcodelist

def print_model(gcodelist,ser,sio):
    print("正在打印")
    i=0
    j=len(gcodelist)
    for line in gcodelist:
        jindu=i/j
        linebit =str.encode(line)
        if line == ";End of Gcode":
            ps.printing = 0
            ps.endprint = 1
            break
        else : 
            ps.printing = 1        
        print(line)
        ser.write(linebit)
        while True:
            read_order = ser.readline()
            if( "ok" in bytes.decode(read_order) or "done" in bytes.decode(read_order)):
                print(bytes.decode(read_order))
                temget = str.encode('M105\n')
                serial.write(temget)                               
                while True:
                    tem_message=serial.readline()
                    print(tem_message)                  
                    if( "ok" in bytes.decode(tem_message) or "done" in bytes.decode(tem_message)):
                        tem_message=bytes.decode(tem_message)
                        tem = re.findall(r"\d+\.?\d*",tem_message)
                        print(tem)
                        if len(tem) == 0:
                            tem = ['0','0','0','0','0']
                        payload_json = {
                                    'id': 1,
                                    'on_off': 1,
                                    'status': {
                                        'chambertemperature':float(tem[0]),
                                        'bedtemperature': float(tem[2])
                                    },
                                    'printing':ps.printing,
                                    'endprint':ps.endprint,
                                    'startprint':ps.startprint,
                                    'jindu':jindu
                                    }
                        sio.emit('status', payload_json)
                        i=i+1
                        print('Send State:')
                        print(payload_json)
                        print(">>>")
                        break
                break      
    ps.endprint = 0
    serial.write(temget)
    while True:
        tem_message=serial.readline()
        if( "ok" in bytes.decode(read_order) or "done" in bytes.decode(read_order)):
            tem_message=bytes.decode(tem_message)
            tem = re.findall(r"\d+\.?\d*",tem_message)
            print(tem)
            if len(tem) == 0:
                tem = ['0','0','0','0','0']
            payload_json = {
                    'id': 1,
                    'on_off': 1,
                    'status': {
                            'chambertemperature':float(tem[0]),
                            'bedtemperature': float(tem[2])
                            },
                    'printing':ps.printing,
                    'endprint':ps.endprint,
                    'startprint':ps.startprint,
                    'jindu':jindu
                    }
    sio.emit('status', payload_json)
    print("打印结束,，发送打印机状态：")
    print(payload_json)
    os.remove("printfile.gcode")
   
    
@sio.on('connect')#连接成功触发汇报树莓派与打印机连接状态
def on_connect():
    print('连接成功')
    if serial.isOpen():  
        time.sleep(8)
        serial.readlines()
        serial.flushOutput()
        printmessage_json = {
                    'id': 1,
                    'on_off': 1,
                    'status': {
                    'chambertemperature':0,
                    'bedtemperature': 0
                    },
                    'printing':ps.printing,
                    'endprint':ps.endprint,
                    'startprint':ps.startprint
                    }
        sio.emit('status', printmessage_json)
        print("打印机上线，发送打印机状态：")
        print(printmessage_json)
    else:
        printmessage_json = {
                    'id': 1,
                    'on_off': 0,
                    'status': {
                    'chambertemperature':0,
                    'bedtemperature': 0,
                    },
                    'printing':ps.printing,
                    'endprint':ps.endprint,
                    'startprint':ps.startprint
                    }
        sio.emit('status', printmessage_json)
        print("打印机连接失败")
        print(printmessage_json)


    
@sio.on('file')#
def on_file(file):
    print("接收到打印文件")
    sio.emit('file','getting' )
    fp = open("printfile.gcode",'w') 
    fp.writelines(file) 
    fp.close() 
    #sio.emit('file','got' )
    filename = "printfile.gcode"
    gcodelist = read_gcode(filename)
    ps.startprint = 1
    ps.printing = 1
    serial.write("M105\n".encode('ascii') )
    time.sleep(0.5)
    tem_message=serial.readline()  
    tem_message=bytes.decode(tem_message)
    tem = re.findall(r"\d+\.?\d*",tem_message)
    time.sleep(0.5)
    print(tem)
    if len(tem) == 0:
        tem = ['0','0','0','0','0']
    payload_json = {
                    'id': 1,
                    'on_off': 1,
                    'status': {
                        'chambertemperature':float(tem[0]),
                        'bedtemperature':float(tem[1])
                    },
                    'printing':ps.printing,
                    'endprint':ps.endprint,
                    'startprint':ps.startprint
                    }
    sio.emit('status', payload_json)
    print(payload_json)    
    ps.startprint = 0
    print("开始打印")  
    print_model(gcodelist,serial,sio)
            
@sio.on('status')
def on_state():
    serial.write("M105\n".encode('ascii') )
    time.sleep(0.5)
    tem_message=serial.readline()
    tem_message=bytes.decode(tem_message)
    tem = re.findall(r"\d+\.?\d*",tem_message)
    time.sleep(1)
    print(tem)
    if len(tem) == 0:
        tem = ['0','0','0','0','0']
    payload_json = {
                'id': 1,
                'status': {
                        'chambertemperature':float(tem[0]),
                        'bedtemperature': float(tem[2])
                },
                'on_off': 1,
                'printing':ps.printing,
                'endprint':ps.endprint,
                'startprint':ps.startprint
                }            
    sio.emit('status', payload_json)
    print("打印机状态发送state")
    
@sio.on('disconnect')#只要在disconnect下发送消息即刻断开连接
def on_disconnect():
    print('重新连接')


sio.connect('http://120.79.148.35:7002')
sio.wait()
