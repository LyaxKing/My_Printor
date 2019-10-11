# -*- coding: utf-8 -*-
from socket import *
import threading

PORT = 9999
HOST = '47.96.95.75'
#HOST = '192.168.1.110'
BUFSIZ = 1024 * 1024
ADDR = (HOST, PORT)


class FileReceiver:
    def __init__(self):
        print('生成客户端')

    def get_file(self, print_center):
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
        print('Try connect.')
        self.tcpCliSock.connect(ADDR)
        while True:
            message_pid = '1' #确认某id的打印机连接成功
            self.tcpCliSock.send(bytes(message_pid, 'utf-8'))#确认连接成功
            print(message)
            data = self.tcpCliSock.recv(BUFSIZ)
            data = data.decode()
            print(data)
            if not data:
                break
            if data == "0":
                print("No File")
                break
            else:
                file_total_size = int(data)
                self.tcpCliSock.send(bytes(message, 'utf-8'))#告知服务器打印文件大小已收到
                print(message)
                received_size = 0
                print("写入文件")
                f = open("printfile.gcode", "wb")
                while received_size < file_total_size:
                    data = self.tcpCliSock.recv(BUFSIZ)
                    f.write(data)
                    received_size += len(data)
                    print(received_size/file_total_size)
                f.close()
                print("Received: ", file_total_size, " ", received_size)
                if file_total_size == received_size:
                    message = '1'
                    self.tcpCliSock.send(bytes(message, 'utf-8'))#告知服务器打印文件接收成功并开始打印
                    print('接收成功！')
                    print_center.print_file_alive = 1
                    break
                else:
                    message = '0'
                    self.tcpCliSock.send(bytes(message, 'utf-8'))
                    print('接收失败！')
        self.tcpCliSock.close()
        print('通讯结束')

    '''def start_listen(self, print_center):
        print('TCPsever on.')
        while True:
            print('waiting for connection...')
            tcpCliSocket, addr = self.tcpSerSock.accept()
            print('...connected from:', addr)
            while True:
                data = tcpCliSocket.recv(BUFSIZ)
                if not data:
                    print('waiting.....')
                    break
                else:
                    file_total_size = int(data.decode())
                    print("Filesize:"+str(file_total_size))
                    received_size = 0
                    fp = open("printfile.gcode", 'w')
                    while received_size <= file_total_size:
                        data = self.tcpSerSock.recv(BUFSIZ)
                        fp.write(data)
                        received_size += len(data)
                        print("已接收:", received_size)
                    fp.close()
                    print("receive done", file_total_size, " ", received_size)
                    if received_size < file_total_size:
                        tcpCliSocket.send('0')
                    else:
                        tcpCliSocket.send('1')
                    print("Start printing")
                    print_center.print_model()
                    break

    def close(self):
        self.tcpSerSock.close()'''