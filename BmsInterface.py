# _*_ coding:UTF-8 _*_
import socket,threading,time
from socket import *
import SocketServer
import xmlrpclib
from ConfigReader import Config


datalist = [] #全局输出状态数据
srvlock = threading.RLock() #线程锁

class BmsIf:
    def __init__(self):
        self.config_obj = Config.singleton()
        self.init_udp_server()
        self.init_udp_client()
        # self.init_bms_control()

    # udp server用于从bms接收
    def init_udp_server(self):
        self.local_addr = (self.config_obj.config.get("LocalUDPServer", "IP"), int(self.config_obj.config.get("LocalUDPServer", "PORT")))
        thread_recv_state = threading.Thread(target=self.recv)
        thread_recv_state.start()

    def recv(self):
        self.recv_sock = socket(AF_INET, SOCK_DGRAM)
        self.recv_sock.bind(self.local_addr)
        global datalist
        while True:
            data, addr = self.recv_sock.recvfrom(1024*1024)
            # print(data)
            srvlock.acquire()
            datalist = data.split("|")
            srvlock.release()
        self.recv_sock.close()

    # udp client用于向bms发送动作
    def init_udp_client(self):
        self.bms_action_sock = socket(AF_INET, SOCK_DGRAM)
        self.bms_action_addr = (self.config_obj.config.get("RemoteUDPserver", "IP"), int(self.config_obj.config.get("RemoteUDPserver", "PORT")))

    def sendto(self, command):
        self.bms_action_sock.sendto(command, self.bms_action_addr)

    # # rpc用于bms的启停
    # def init_bms_control(self):
    #     self.bms_control_proxy = xmlrpclib.ServerProxy(self.config_obj.config.get("RemoteRPCServer", "HTTP"))
    #
    # # 1: start; 2: stop; 3: reboot
    # def send_ctrl_cmd(self, cmd):
    #     self.bms_control_proxy.RPCserverForGameserver(cmd)