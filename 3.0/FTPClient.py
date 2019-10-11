# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:24:35 2019

@author: HP
"""
import ftplib
# 关于FTP的操作都在这个包里边。


class SocketGetGcode:
# 三部分精确表示在ftp服务器上的某一个文件
    HOST = "ftp.acc.umu.se"
    DIR = 'Public/EFLIB/'
    FILE = 'printfile.gcode'


# 1. 客户端链接远程主机上的FTP服务器
def connect_ftp_sever(self):
    try:
        self.f = ftplib.FTP()
        # 链接主机地址
        self.f.connect(self.HOST)
    except Exception as e:
        print(e)
        exit()
    print("***Connected to host {0}".format(self.HOST))


# 2. 客户端输入用户名和密码（或者“anonymous”和电子邮件地址）
def login(self):
    try:
        # 登录如果没有输入用户信息，则默认使用匿名登录
        self.f.login()
    except Exception as e:
        print(e)
        exit()
    print("***Logged in as 'anonymous'")


# 3. 客户端和服务器进行各种文件传输和信息查询操作
def change_file_dir(self):
    try:
        self.f.cwd(self.DIR)# 更改当前目录到指定目录
    except Exception as e:
        print(e)
    exit()
    print("*** Changed dir to {0}".format(self.DIR))


def download_gcode(self):
    try:
    # 从FTP服务器上下载文件
    # 第一个参数是ftp命令，第二个参数是回调函数
    # 此函数的意思是，执行RETR命令，下载文件到本地后，运行回调函数
        self.f.retrbinary('RETR {0}'.format(self.FILE), open(self.FILE, 'wb').write)
    except Exception as e:
        print(e)
        exit()
    # 4. 客户端从远程FTP服务器退出，结束传输
    self.f.quit()




