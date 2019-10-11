# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:24:35 2019

@author: HP
"""
import Printor_control
import socketio
import serial


portname = "COM6"
baudrate = 115200
printid = '1'
tem_position = [0, 2]
sio = socketio.Client()
ps = Printor_control.print_state(printid, portname, baudrate, sio, tem_position)
sio.connect('tcp://47.96.95.75:7002')


@sio.on('connect')
def on_connect():
    print('连接成功')
    if ps.start():
        statue_json = ps.get_statue_json()
        sio.emit('status', statue_json)
        print("打印机上线，发送打印机状态：")
    else:
        statue_json = ps.get_statue_json()
        sio.emit('status', statue_json)
        print("打印机连接失败")
    print(statue_json)


@sio.on('file')
def on_file(file):
    print("接收到打印文件")
    fp = open("printfile.gcode", 'w')
    fp.writelines(file) 
    fp.close() 
    gcodelist = ps.read_gcode()
    ps.startprint = 1
    ps.printing = 1
    statue_json = ps.get_statue_json()
    sio.emit('status', statue_json)
    print(statue_json)
    ps.startprint = 0
    print("开始打印")  
    ps.print_model(gcodelist)
    
   
@sio.on('status')
def on_state():
    ps.tem_get()         
    statue_json = ps.get_statue_json()
    sio.emit('status', statue_json)
    print("打印机状态发送state")
    print(statue_json)


@sio.on('disconnect')#只要在disconnect下发送消息即刻断开连接
def on_disconnect():
    print('重新连接')


sio.wait()    

