# -*- coding:utf-8 -*-

import time
import FlyCtrl
import threading

if __name__ == "__main__":
    # thread_fly = threading.Thread(target = FlyCtrl.keep_levelflight)
    thread_fly = threading.Thread(target = FlyCtrl.random_fly)
    thread_fly.start()
    # time.sleep(0.1)
    FlyCtrl.bms_interface.init_bms_control()
    while True:
        FlyCtrl.start()
        FlyCtrl.bms_interface.send_ctrl_cmd('1')
        time.sleep(100)
        FlyCtrl.bms_interface.send_ctrl_cmd('2')
        FlyCtrl.stop()