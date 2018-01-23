# _*_ coding:UTF-8 _*_


import AiInterface
import FlyCtrl
import threading


if __name__ == "__main__":
    # FlyCtrl.initCombat()
    # FlyCtrl.initFly()
    FlyCtrl.fly_initialization()
    # thread_fly = threading.Thread(target = FlyCtrl.keep_levelflight)
    # thread_fly = threading.Thread(target = FlyCtrl.fly_test)
    thread_fly = threading.Thread(target=FlyCtrl.random_fly())
    thread_fly.start()
    AiInterface.register_rpc()  # 注册rpc服务