# _*_ coding: UTF-8 _*_

import time, threading, json, xmlrpclib
import math
from ConfigReader import Config
from SimpleXMLRPCServer import SimpleXMLRPCServer
import FlyCtrl
import my_config
import LockonInterface

srvlock = threading.RLock() #线程锁

# **********************************************************************************************************************
# auto open,pause and close

def gamectrlFunc(gamectrl=-1): #auto_open & close : "1":--start "2": --pause  "3": --- reset
    global done,self_info,enemy_info,reward_total
    if gamectrl=="3":
        FlyCtrl.Input = 0
        FlyCtrl.Input1 = 0
        self_info={}
        enemy_info=[]
        reward_total = 0
        done=False
    if gamectrl=="1" or gamectrl=="2":
        srvlock.acquire()
        datalist=[]
        srvlock.release()
        FlyCtrl.jiali=0
    return proxy.RPCserverForGameserver(gamectrl)

# **********************************************************************************************************************
# get_feedback
#
# def pre_get_feedback(): # to get info we need from detailed info phrase
#
#     # srvlock.acquire()
#     if len(LockonInterface.datalist) > 0:
#         global self_flag
#         try:
#             self_flag = LockonInterface.datalist[0] # frame time for AI fail judgement
#             selfdata_v = LockonInterface.datalist[3]
#             selfdata = LockonInterface.datalist[8]
#             # enemydata = LockonInterface.datalist[14]
#             enemydata = FlyCtrl.parsejson_enermy_detail()
#             print (enemydata)
#             enemy_flag = LockonInterface.datalist[17]  # enemy fail judgement
#             srvlock.release()
#             return self_flag, selfdata_v, selfdata, enemydata, enemy_flag
#         except ZeroDivisionError, e:
#             srvlock.release()
#     # srvlock.release()
#     return None, None, None, None, None


def pre_get_feedback(): # to get info we need from detailed info phrase

    #self_flag = 1
    selfdata_v = FlyCtrl.parsejson_speed()
    selfdata = FlyCtrl.parsejson_selfinfor()
    # enemydata = LockonInterface.datalist[14]
    enemydata = FlyCtrl.parsejson_enermy_detail()
    print (enemydata)
    #enemy_flag = 1  # enemy fail judgement
    return selfdata_v, selfdata, enemydata

# ......................................................................................................................

def get_feedback():

    self_info = {}
    enemy_fighter_info = {}
    enemy_missile_info_all = []
    enemy_missile_info ={}

    reward = 0
    reward_outrange = 0
    reward_kill = 0

    done = False
    done_outrange = False
    done_kill = False

    # center of the combat zone
    x0 = -308790.21136857
    z0 = 645985.5625
    y0 = 5000
    r = 50000 # radius

    # self_flag, selfdata_v, selfdata, enemydata, enemy_flag = pre_get_feedback() # to get all the information
    selfdata_v, selfdata, enemydata = pre_get_feedback()  # to get all the information

    # ..................................................................................................................
    # AI (self) information
    global self_state, self_x, self_y, self_z

    #while True:
    if selfdata_v != None and selfdata != None:
        # self_data_v = json.loads(selfdata_v)
        # self_data = json.loads(selfdata)
        self_data_v = selfdata_v
        self_data = selfdata

        self_x = self_data["Position"]["x"] # to do the calculations about distance or stuff
        self_y = self_data["Position"]["y"] # height
        self_z = self_data["Position"]["z"]
        self_pitch = self_data["Pitch"]  # pai/2
        self_yaw = self_data["Heading"] # Yaw: 2*pai
        self_velocity = self_data_v # not more than sound speed, namely 340 m/s

        self_info_x = self_x / -880000 # to store in the buffer
        self_info_y = self_y / 10000 # height
        self_info_z = self_z / 880000
        self_info_pitch = self_pitch / 1.57 # pai/2
        self_info_yaw = self_yaw / 6.28 # Yaw: 2*pai
        self_info_volecity = self_velocity / 340 # not more than sound speed, namely 340 m/s

        self_state = [self_info_x,self_info_y,self_info_z,self_info_pitch,self_info_yaw,self_info_volecity]

        # AI done_outrange information judgement
        D_AI = math.sqrt(math.pow((self_x - x0), 2) + math.pow((self_z - z0), 2))
        my_config.logger.debug('D_AI:%s' % D_AI)
        if D_AI > r or self_y > 10000 or FlyCtrl.parsejson_altRad() < 10 : # include the crash info
            done_outrange = True
            my_config.logger.info('Done for AI outrange !')
            reward_outrange = -100
    else:
        my_config.logger.warn('Warning: No Self Information !!! Trying to reopen...')

    # ..................................................................................................................
    # Enemy information
    global enemy_fighter_state, enemy_missile_state, enemy_fighter_x, enemy_fighter_y, enemy_fighter_z
    enemy_data = {}
    missile_distance_list = []
    enemy_missile_state = []

    def distance_cal(x1,y1,z1,x2,y2,z2):
        distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2) + math.pow((z2 - z1), 2))
        return distance

    # while True: # keep inspecting whether both the fighter and missile info are available

    if enemydata != '{"Emitters":[],"Mode":0}': # enemy info is available
        # enemy_data = json.loads(enemydata)
        enemy_data = enemydata
        #print('%s missle detected' % (len(enemy_data) - 1))
        print(enemy_data)

        for i, element in enumerate(enemy_data, start=0):
            if enemy_data[i]['Type']['level3'] == 1:  # Fighter

                enemy_fighter_x = enemy_data[i]["Position"]["x"]
                enemy_fighter_y = enemy_data[i]["Position"]["y"]
                enemy_fighter_z = enemy_data[i]["Position"]["z"]
                enemy_fighter_pitch = enemy_data[i]["Pitch"]
                enemy_fighter_yaw = enemy_data[i]["Heading"]

                enemy_fighter_info_x = enemy_fighter_x / -880000
                enemy_fighter_info_y = enemy_fighter_y / 10000
                enemy_fighter_info_z = enemy_fighter_z / 880000
                enemy_fighter_info_pitch = enemy_fighter_pitch / 1.57
                enemy_fighter_info_yaw = enemy_fighter_yaw / 6.28

                enemy_fighter_state = [enemy_fighter_info_x,enemy_fighter_info_y,enemy_fighter_info_z,
                                       enemy_fighter_info_pitch,enemy_fighter_info_yaw]

            elif enemy_data[i]['Type']['level3'] == 7:  # AA missile
                print ('missile found')
                enemy_missile_info_all.append(enemy_data[i])

        if len(enemy_missile_info_all) == 0:
            time.sleep(0.1)
            # continue

        for j, element1 in enumerate(enemy_missile_info_all):
            missile_distance = distance_cal(self_x, self_y, self_z,
                                            enemy_missile_info_all[j]["Position"]["x"],
                                            enemy_missile_info_all[j]["Position"]["y"],
                                            enemy_missile_info_all[j]["Position"]["z"])
            missile_distance_list.append(missile_distance)
        if missile_distance_list != []:
            missile_distance_min = missile_distance_list.index(min(missile_distance_list))
            enemy_missile_data = enemy_missile_info_all[missile_distance_min] # the missile with the max threat

            enemy_missile_x = enemy_missile_data["Position"]["x"]
            enemy_missile_y = enemy_missile_data["Position"]["y"]
            enemy_missile_z = enemy_missile_data["Position"]["z"]
            enemy_missile_pitch = enemy_missile_data["Position"]["Pitch"]
            enemy_missile_yaw = enemy_missile_data["Position"]["Yaw"]

            enemy_missile_info_x = enemy_missile_x / -880000
            enemy_missile_info_y = enemy_missile_y / 10000
            enemy_missile_info_z = enemy_missile_z / 880000
            enemy_missile_info_pitch = enemy_missile_pitch / 1.57
            enemy_missile_info_yaw = enemy_missile_yaw / 6.28

            enemy_missile_state = [enemy_missile_info_x,enemy_missile_info_y,enemy_missile_info_z,
                                   enemy_missile_info_pitch,enemy_missile_info_yaw]
            # break

        # enemy done_outrange information judgement
        D_enemy = math.sqrt(math.pow((enemy_fighter_x - x0),2) + math.pow((enemy_fighter_z - z0),2))
        my_config.logger.debug('D_Bot:%s' % D_enemy)
        if D_enemy > r or enemy_fighter_y > 10000:
            done_outrange = True
            my_config.logger.info('Done for enemy outrange !')
            reward_outrange = 100

        # if the distance between AI and Bot is less than 10,000m, done !
        D_between = math.sqrt(math.pow((enemy_fighter_x - self_x),2) +
                              math.pow((enemy_fighter_z - self_z),2))
        my_config.logger.debug('D_between:%s' % D_between)
        if D_between <= 10000:
            done_outrange = True # if distance between AI and enemy < 10000m, done

    state = self_state + enemy_fighter_state + enemy_missile_state

    # ..................................................................................................................
    # kill judgement
    # AI
    # current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    #
    # lastframe_time = json.loads(self_flag)["systime"]
    # if int(current_time) - int(lastframe_time) > 10:
    #     done_kill = True
    #     my_config.logger.info('Done for Bot kill AI !')
    #     reward_kill = -1
    # else:
    #     pass
    # # enemy:
    # if enemy_flag == 'null': # bug in it ? change to time ?
    #     done_kill = True
    #     my_config.logger.info('Done for AI kill Bot !')
    #     reward_kill = 1
    # else:
    #     pass
    # # ..................................................................................................................
    # reward and done information
    reward = reward_outrange + reward_kill - 0.01 # minus 0.1 per step
    my_config.logger.debug('reward_outrange:%s, reward_kill:%s' % (reward_outrange, reward_kill))

    if  done_outrange == True or done_kill == True:
        done = True
        my_config.logger.debug('done_outrange:%s, done_kill:%s' % (done_outrange, done_kill))
    else:
        done = False
    # ..................................................................................................................

    my_config.logger.debug('state:%s, reward:%s, done:%s' % (state, reward, done))
    return state, reward, done

# **********************************************************************************************************************
def step(action):
    FlyCtrl.set_flag_break(action)

def get_flag_entrance():
    return FlyCtrl.get_flag_entrance()
# **********************************************************************************************************************
# Main function
Configobj = Config.singleton()
proxy = xmlrpclib.ServerProxy(Configobj.config.get("RemoteRPCServer", "HTTP")) #rpc调用自动开局程序  "http://localhost:8000/"

def RPCregister():
    IP = Configobj.config.get("LocalRPCServer", "IP")
    PORT=Configobj.config.get("LocalRPCServer", "PORT")
    server = SimpleXMLRPCServer((IP,int(PORT)),allow_none=True)  # 确定URL和端口
    server.register_function(gamectrlFunc, "gamectrlFunc")  # 注册is_even函数
    server.register_function(step, "step")  # 注册is_even函数
    server.register_function(get_feedback, "get_feedback")  # 注册is_even函数
    server.register_function(get_flag_entrance, "get_flag_entrance")
    server.serve_forever()  # 启动服务器,并使其对这个连接可用