# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:57:51 2019

@author: HP
"""
import PCC
import FR
import SR
import threading
import time

baudrate = 115200
printid = '1'
tem_position = [0, 2]
portname = '/dev/ttyUSB0'
#portname = 'COM6'

def state_send_thread(print_center, state_reportor):
    while True:
        if print_center.printing == 0:
            data = print_center.get_statue_json()
        state_reportor.senddata(data)
        print(">>>Statue>>>")


def get_file_thread(print_center, file_receiver):
    while True:
        if print_center.alive == 1 and print_center.printing == 0:
            file_receiver.get_file(print_center)
            if print_center.print_file_alive == 1:
                print('开始打印！')
                p = threading.Thread(target=print_center.print_model)
                p.start()
        time.sleep(10)




def main():
    pc = PCC.PrintControl(printid, portname, baudrate, tem_position)
    pc.printor_alive()
    fr = FR.FileReceiver()
    sr = SR.StatueReportor()
    ss = threading.Thread(target=state_send_thread, args=(pc, sr))
    gft = threading.Thread(target=get_file_thread, args=(pc, fr))
    ss.start()
    gft.start()
    ss.join()
    gft.join()


if __name__ == '__main__':
    main()

