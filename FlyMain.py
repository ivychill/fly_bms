# -*- coding:utf-8 -*-

import time
import FlyCtrl
import threading

if __name__ == "__main__":
    # thread_fly = threading.Thread(target = FlyCtrl.keep_levelflight)
    thread_fly = threading.Thread(target = FlyCtrl.random_fly)
    thread_fly.start()
    # time.sleep(0.1)
    while True:
        FlyCtrl.start()
        time.sleep(100)
        FlyCtrl.stop()