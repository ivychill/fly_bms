# _*_ coding:UTF-8 _*_

from ConfigReader import Config
import LockonInterface
import AiInterface
import FlyCtrl
import threading


if __name__ == "__main__":
    #raw_input("Press any key to began...\n")
    Configobj = Config.singleton()
    LockonInterface.runserver(Configobj.config.get("LocalUDPServer", "IP"), int(Configobj.config.get("LocalUDPServer", "PORT")))
    LockonInterface.initudpclient(Configobj.config.get("RemoteUDPserver", "IP"), int(Configobj.config.get("RemoteUDPserver", "PORT")))
    # FlyCtrl.initCombat()
    # FlyCtrl.initFly()
    FlyCtrl.fly_initialization()
    # thread_fly = threading.Thread(target = FlyCtrl.keep_levelflight)
    thread_fly = threading.Thread(target = FlyCtrl.fly_test)
    thread_fly.start()
    AiInterface.RPCregister() #注册rpc服务