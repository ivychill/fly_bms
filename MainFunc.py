# _*_ coding:UTF-8 _*_


import AiInterface
import FlyCtrl
import threading
from my_config import *


if __name__ == "__main__":
    # FlyCtrl.initCombat()
    FlyCtrl.joystick_initialization()
    FlyCtrl.fly_initialization()
    # thread_fly = threading.Thread(target = FlyCtrl.keep_levelflight)
    thread_fly = threading.Thread(target = FlyCtrl.fly_test)
    thread_fly.start()
    thread_radar = threading.Thread(target=FlyCtrl.scan_and_lock)
    # # # thread_fly = threading.Thread(target=FlyCtrl.random_fly)
    thread_radar.start()

    # AiInterface.register_rpc()  # 注册rpc服务