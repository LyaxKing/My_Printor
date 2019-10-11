# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:57:51 2019

@author: HP
"""
import PrintControl
import FTPClient
import AliyunMqtt
import time
import _thread

socket_host_name = 'http://120.79.148.35:7002'
productkey = 'a1RJRghvKOW'
devicename = 'Yinba_1'
devicesecret = 'WUmFrsbg1IWxPPHO1LndP6cx7BPrudk3'
portname = ""
baudrate = 115200
printid = '1'
tem_position = [0, 2]

options = {
    'productKey': 'a1RJRghvKOW',
    'deviceName': 'Yinba_1',
    'deviceSecret': 'WUmFrsbg1IWxPPHO1LndP6cx7BPrudk3',
    'port': 1883,
    'host': 'iot-as-mqtt.cn-shanghai.aliyuncs.com'
}

host = options['productKey'] + '.' + options['host']


def try_mqtt():
    while True:
        try:
            mqttclient = AliyunMqtt.MqttClient(options, host)
            return mqttclient
        except Exception as e:
            print(e)
            continue


def printor_is_on():
    while True:
        try:
            printcontrol = PrintControl.PrintControl(printid, portname, baudrate, tem_position)
            if printcontrol.is_start():
                printcontrol.tem_get()
                s_json = printcontrol.get_statue_json()
                return printcontrol, s_json
        except Exception as e:
            print(e)
            continue


def get_and_print_gcode(printcontrol, mqttclient):
    FTPClient.connect_ftp_sever()
    FTPClient.login()
    FTPClient.change_file_dir()
    FTPClient.download_gcode()
    mqttclient.check_file = 0
    printcontrol.print_model()


def loop_pc_repotor(mqttclient, printcontrol):
    while True:
        time.sleep(3)
        printcontrol.tem_get()
        statue_json = printcontrol.get_statue_json()
        mqttclient.pubilish_status(statue_json)
        if mqttclient.check_file:
            try:
                if thread.isAlive():
                   continue
                else :
                   thread.join()
            except Exception as e:
                print(e)
                thread = thread.start_new_thread(get_and_print_gcode,(printcontrol, mqttclient,))




if __name__ == 'main':
    mc = try_mqtt()
    pc, statue_json = printor_is_on()
    mc.pubilish_status(statue_json)
    loop_pc_repotor(mc,pc)
