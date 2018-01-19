# _*_ coding:UTF-8 _*_
import socket,threading,time
from socket import *
import SocketServer


datalist = [] #全局输出状态数据
srvlock = threading.RLock() #线程锁
udpsock =socket(AF_INET,SOCK_DGRAM)


def recvFunc(Host, Port):
    udpsock.bind((Host, Port))
    global datalist
    while True:
        data,addr = udpsock.recvfrom(1024*1024)
        # print(data)
        srvlock.acquire()
        datalist = data.split("|")
        # datatime = time.time()
        # print(datatime)
        srvlock.release()
    udpsock.close()



def runserver(Host, Port):
    t1 = threading.Thread(target=recvFunc, args=(Host, Port))
    t1.start()



# udp client用于向lockon发送动作
udpCliSock = socket(AF_INET, SOCK_DGRAM)  #全局input发送套接字
ADDR=()  #全局input发送

def initudpclient(host,port):
    global ADDR
    ADDR = (host, port)

def sendto(command):
    udpCliSock.sendto(command, ADDR)