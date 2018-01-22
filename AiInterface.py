# -*- coding: utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
import FlyCtrl

def register_rpc():
    server = SimpleXMLRPCServer(("192.168.20.129", 4022), allow_none=True)
    # server = SimpleXMLRPCServer(("192.168.24.116", 4022), allow_none=True)
    # server.register_function(gamectrlFunc, "gamectrlFunc")
    server.register_function(get_fly_state, "get_fly_state")
    server.register_function(start, "start")
    server.register_function(stop, "stop")
    server.register_function(reboot, "reboot")
    server.serve_forever()  # 启动服务器,并使其对这个连接可用

#
def get_fly_state():
    z = FlyCtrl.parsejson_altRad()
    speed = FlyCtrl.parsejson_speed()
    pitch = FlyCtrl.parsejson_pitch()
    yaw = FlyCtrl.parsejson_yaw()

    return z, speed, pitch, yaw

# TODO:开局
def start():
    FlyCtrl.start()

# TODO:终止
def stop():
    FlyCtrl.stop()

# TODO:终止
def reboot():
    FlyCtrl.reboot()