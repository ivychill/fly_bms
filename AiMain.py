# -*- coding:utf-8 -*-

import AiInterface
import FlyCtrl
import threading

if __name__ == "__main__":
    # thread_fly = threading.Thread(target = FlyCtrl.keep_levelflight)
    thread_fly = threading.Thread(target = FlyCtrl.random_fly)
    thread_fly.start()
    AiInterface.register_rpc()  # 注册rpc服务