# -*- coding: utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
import FlyCtrl
import time
from my_config import *

def register_rpc():
    # server = SimpleXMLRPCServer(("192.168.20.129", 4022), allow_none=True)
    logger.warn("ai interface starting...")
    server = SimpleXMLRPCServer(("192.168.20.129", 4022), allow_none=True)
    # server.register_function(gamectrlFunc, "gamectrlFunc")
    server.register_function(get_fly_state, "get_fly_state")
    server.register_function(start, "start")
    server.register_function(stop, "stop")
    server.register_function(prepare, "prepare")
    # server.register_function(reboot, "reboot")
    server.serve_forever()  # 启动服务器,并使其对这个连接可用

#
def get_fly_state():
    z = FlyCtrl.parsejson_altRad()
    speed = FlyCtrl.parsejson_speed()
    pitch = FlyCtrl.parsejson_pitch()
    yaw = FlyCtrl.parsejson_yaw()
    logger.info("z: %s, speed: %s, pitch: %s, yaw: %s" % (z, speed, pitch, yaw))

    return z, speed, pitch, yaw

def start():
    logger.info("started...")
    FlyCtrl.start()

def stop():
    FlyCtrl.stop()

# def reboot():
#     FlyCtrl.reboot()

def prepare():
    FlyCtrl.fly_initialization()