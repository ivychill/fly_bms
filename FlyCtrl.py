#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math,thread,time
import threading
import json,sys
import BmsInterface
import random
from my_config import *
import xmlrpclib



# 相关参数获取

##################
#敌机时间参数
def get_datatime():
    ssss=""
    BmsInterface.srvlock.acquire()
    ssss= BmsInterface.datatime
    BmsInterface.srvlock.release()

    return ssss

#我机角度参数pitch，bank(roll),yaw
def parsejson_pitch():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[0])
            BmsInterface.srvlock.release()
            return obj['pitch']
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()
    return -100

def parsejson_bank():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[0])
            BmsInterface.srvlock.release()
            return obj['roll']
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()

    return -100

def parsejson_yaw():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[0])
            BmsInterface.srvlock.release()
            return obj['yaw']
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()
    return -100


def parsejson_alpha():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[0])
            BmsInterface.srvlock.release()
            return obj['alpha']*math.pi/180
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()
    return -100

#速度矢量符位置
def speed_vector():
    v_a = parsejson_pitch() - parsejson_alpha()
    return v_a

#获取海拔高度
def parsejson_altBar():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[0])
            BmsInterface.srvlock.release()
            return obj['altBar']
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()
    return -100

#获取地面高度
def parsejson_altRad():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[0])
            BmsInterface.srvlock.release()
            return -obj['z']
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()
    return -100

#获取速度
def parsejson_speed():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[0])
            BmsInterface.srvlock.release()
            return obj['kias']
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()

    return -100

#获取扫描（视觉系统）信息
def parsejson_targetscan():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[12])
            BmsInterface.srvlock.release()
            return obj
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()

    return None

#获取预警敌机信息
def parsejson_enermy():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[13])
            BmsInterface.srvlock.release()
            if obj is not None:
                lenth=len(obj)
                if lenth>1:
                    return obj["Emitters"]
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()
    return None

#获取详细敌机信息
def parsejson_enermy_detail():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[14])
            if obj is not None:
                BmsInterface.srvlock.release()
                return obj
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
            return None
    BmsInterface.srvlock.release()
    return None

#获取目标信息
def parsejson_target():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[10])

            if obj is not None:
                BmsInterface.srvlock.release()
                return obj
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
            return None
    BmsInterface.srvlock.release()
    return None

#获取已锁定目标信息
def parsejson_lockedtarget():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[11])
            if obj is not None:
                BmsInterface.srvlock.release()
                return obj
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
            return None
    BmsInterface.srvlock.release()
    return None

#获取我机信息
def parsejson_selfinfor():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[8])
            if obj is not None:
                BmsInterface.srvlock.release()
                return obj
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
            return None
    BmsInterface.srvlock.release()
    return None


def parsejson_G():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[2])
            if obj is not None:
                BmsInterface.srvlock.release()
                return obj
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
            return None
        BmsInterface.srvlock.release()
    return None

#获取挂载信息
def parsejson_loadinfor():
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[15])
            if obj is not None:
                BmsInterface.srvlock.release()
                return obj
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
            return None
    BmsInterface.srvlock.release()
    return None

# def parsejson_enemyid():
#     BmsInterface.srvlock.acquire()
#     if len(BmsInterface.datalist)>0:
#         try:
#             obj = json.loads(BmsInterface.datalist[17])
#             if obj is not None:
#                 BmsInterface.srvlock.release()
#                 return obj
#         except ZeroDivisionError,e:
#             BmsInterface.srvlock.release()
#             return None
#     BmsInterface.srvlock.release()
#     return None


#飞行姿态控制，pitch，roll
t_roll=time.time()
t_config = time.time()
e_roll_last=0
e_roll_sum = 0
delta_e = 0
e = 0
def keep_roll(roll):
    global t_roll,e_roll_last,e,e_roll_sum,delta_e,t_config
    e = roll - parsejson_bank()
    e_roll_sum = e_roll_sum + e
    delta_e = e - e_roll_last

    if e > math.pi:
        e = e - 2 * math.pi
    if e < -math.pi:
        e = e + 2 * math.pi
    if (time.time() - t_roll) > 0.12:
        if abs(e)>0.9*math.pi or abs(roll) == math.pi:
            Kp1 = 0.333
            Ki1 =0.00000
            Kd1 = 0
            # print '111'0.334
            # command2 = "y" + ":" + str(32767 * (0.215 * (abs(roll) + 0.03) + 1) / 2)
            # LockonInterface.sendto(command2)
        else:
            Kp1 = 0.581
            Ki1 = 0.00000
            Kd1 = 0.25
            command2 = "y" + ":" + str(32767 * (0.215 * (abs(roll) + 0.01) + 1) / 2)
            bms_interface.sendto(command2)
        #可用参数
        # Kp1 = 0.581
        # Ki1 = 0.00000
        # Kd1 = 0.25
        # Kp1 =0.38
        # Ki1 =0.000005
        # Kd1 = 0.18
        # Kp2 = 0.39
        # Ki2 = 0.00001
        # Kd2 = 0.18
        # command2 = "y" + ":" + str(32767 * (0.216 * (abs(roll) + 0.03) + 1) / 2)
        # if e > 0:
        #
        #     a = 0.33 * e + 0.00000* e_roll_sum + 0.18* (delta_e)
        # else:
        #     a = 0.4 * e + 0.00000 * e_roll_sum + 0.14 * (e - e_roll_last)
        # if e > 0:

        a = Kp1 * e + Ki1* e_roll_sum + Kd1* (delta_e)

        if a < -1:
            a = -1
        if a > 1:
            a = 1

        logger.debug('PID：a = %s * e + %s* e_roll_sum + %s* (delta_e)' % (Kp1, Ki1, Kd1))
        logger.debug('比例:%s' % e)
        logger.debug('积分:%s' % e_roll_sum)
        logger.debug('微分:%s' % delta_e)
        logger.debug('speed:%s' % parsejson_speed())
        logger.debug('roll:%s' % parsejson_bank())

        command1 = "x" + ":" + str(32767*(a+1)/2.0)
        bms_interface.sendto(command1)

        t_roll = time.time()
        e_roll_last = e


t_va=time.time()
e_va_last=0
e_va_sum = 0
def keep_speed_vector(va):
    global t_va,e_va_last,e_va_sum,a
    e=va-speed_vector()
    e_va_sum = e_va_sum + e
    if  e>math.pi:
        e=e-2*math.pi
    if e< -math.pi:
        e=e+2*math.pi
    if (time.time()-t_va) >0.12:
        # a = 0.95 * e + 0.12 * (e - e_va_last)
        # a = 1*e + 0.12* (e - e_va_last)
        # a = 1.18*e + 0.1* (e - e_va_last)###（0.25直连参数）

        a = 1.6 * e + 0.1 * (e - e_va_last)
        if a < -1:
            a = -1
        if a > 1:
            a = 1
        command = "y" + ":" + str(32767*(a+1)/2.0)
        bms_interface.sendto(command)
        t_va=time.time()
        e_va_last = e


t_pitch=time.time()
e_pitch_last=0
def keep_pitch(pitch):
    global t_pitch,e_pitch_last
    e=pitch-parsejson_pitch()
    if  e>math.pi:
        e=e-2*math.pi
    if e< -math.pi:
        e=e+2*math.pi
    if (time.time()-t_pitch) >0.05:

        a = 3*e+ 6* (e - e_pitch_last)
        if parsejson_speed()>310:
            a=0.5*a
        if a < -1:
            a = -1
        if a > 1:
            a = 1
        command = "2001" + "," + str(a)
        bms_interface.sendto(command)
        t_pitch=time.time()
        e_pitch_last = e

#地面高度控制
def keep_altrad(target_altrad):
    e=target_altrad-parsejson_altRad()
    Va_command = (0.35 / 2000) * e
    if Va_command > 0.35:
        Va_command = 0.35
    if Va_command < -0.35:
        Va_command = -0.35
    keep_speed_vector(Va_command)

#海拔高度控制
def keep_altbar(target_altbar):
    e=target_altbar-parsejson_altBar()
    pitch_command=(0.6/2000)*e
    if pitch_command > 0.6:
        pitch_command = 0.6
    if pitch_command < -0.6:
        pitch_command = -0.6
    if parsejson_altRad() < 500:
        pitch_command = 0.5
        print "高度小于500", parsejson_altRad()
    keep_pitch(pitch_command)

#加速控制
jiali=0
def speedup(speed):
    global jiali
    if parsejson_speed() < speed-10 and jiali==0:
        bms_interface.sendto("z:0")
        jiali=1
    if parsejson_speed() > speed and jiali==1:
        bms_interface.sendto("z:21000")   #16537
        jiali=0




## yaw在(0,2*pi)之间取值
t_yaw_pitch=time.time()
yaw_last=parsejson_yaw()
reach_yaw=0
n_roll=0
a_roll=0

##转弯
def keep_yaw_Va(yaw,Va):
    global t_yaw_pitch,yaw_last,reach_yaw,n_roll,a_roll
    my_yaw=parsejson_yaw()
    e_yaw = yaw - my_yaw
    if e_yaw > math.pi:
        e_yaw = e_yaw - 2 * math.pi
    if e_yaw < -math.pi:
        e_yaw = e_yaw + 2 * math.pi
    a = 7 * e_yaw
    speed=parsejson_speed()
    my_Va = speed_vector()
    if speed>430:
        tresh=1.1
        if my_Va<0:
            tresh = 1
    else:
        tresh = 1.05
        if my_Va<0:
            tresh = 0.8

    if a > tresh:
        a = tresh
    if a < -tresh:
        a = -tresh
    keep_roll(a)
    keep_speed_vector(Va)


#盘旋
def spiral(roll,Va):

    bms_interface.sendto("z:0")
    keep_roll(roll)
    keep_speed_vector(Va)


t_commandx=time.time()
t_commandy=time.time()
move_x=0
move_y=0
fire_flag = 0
t_suoding=time.time()
#if abs>40
fire_event = threading.Event()
def scan_and_lock():
    global t_commandx,t_commandy,t_suoding,fire_flag

    while 1:

        td_position = get_td()
        enemy_position = get_enemy_coord()
        time.sleep(0.1)
        print 'td_position:', td_position
        # print 'enemy_position:', enemy_position
        #
        # while td_position ==[0,0] or enemy_position ==[0,0]:
        #     td_position, num_up, num_down = get_td()
        #     enemy_position = get_enemy_coord()
        #     # print 'td_position:', td_position
        #     # print 'enemy_position:', enemy_position
        #     # print '33'

        if td_position is not None and enemy_position is not None:
            # td_position, num_up, num_down = get_td()
            # enemy_position = get_enemy_coord()
            # print 'td_position:', td_position
            # print 'enemy_position:', enemy_position

            # while abs(enemy_position[0]-td_position[0])> 40:
            if abs(enemy_position[0] - td_position[0]) > 40:
                if (enemy_position[0]-td_position[0]) > 0:
                    bms_interface.sendto("K:104")
                    time.sleep(0.25)
                else:
                    bms_interface.sendto("K:103")
                    time.sleep(0.25)

            else:
                if (enemy_position[0]-td_position[0]) > 0:
                    # if (time.time() - t_commandx) > 0.02:
                    #     bms_interface.sendto("K:104")
                    #     t_commandx= time.time()
                    bms_interface.sendto("K:104")
                    time.sleep(0.35)
                else:
                    # if (time.time() - t_commandx) > 0.02:
                    #     bms_interface.sendto("K:103")
                    #     t_commandx = time.time()
                    bms_interface.sendto("K:103")
                    time.sleep(0.35)



            # while abs(enemy_position[1]-td_position[1])> 40:
            if abs(enemy_position[1] - td_position[1]) > 40:
                if (enemy_position[1]-td_position[1]) > 0:
                    bms_interface.sendto("K:102")
                    time.sleep(0.25)
                else:
                    bms_interface.sendto("K:101")
                    time.sleep(0.25)
            else:
                if (enemy_position[1]-td_position[1]) > 0:
                    # if (time.time() - t_commandx) > 0.02:
                    #     bms_interface.sendto("K:102")
                        # t_commandx= time.time()
                    bms_interface.sendto("K:102")
                    time.sleep(0.35)
                else:
                    # if (time.time() - t_commandx) > 0.02:
                    #     bms_interface.sendto("K:101")
                    #     t_commandx = time.time()
                    bms_interface.sendto("K:101")
                    time.sleep(0.35)


            dis = math.sqrt((enemy_position[0] - td_position[0]) ** 2 + (enemy_position[1] - td_position[1]) ** 2 )


            if dis < 30*1.414 :
                # print '锁定'and (time.time()-t_suoding)>0.2
                bms_interface.sendto("K:281")
                # bms_interface.sendto("K:299")
                # t_suoding=time.time()

        index = get_Index()
        print 'index_fire: ',index
        rpi_bar = get_Rpi()
        print 'rpi_bar_fire: ', rpi_bar
        rtr_bar = get_Rtr()
        print 'rtr_bar_fire: ', rtr_bar
        if index is not None and rpi_bar is not None and rtr_bar is not None:
            if (fire_flag ==0) and ((index > rpi_bar) or (index > rtr_bar)):
                print '11111'
                fire_flag = 1
                bms_interface.sendto("K:299")
                fire_event.set()

            # print '2222'


            # if index > rtr_bar:
            #     bms_interface.sendto("K:299")

# add 2018-01-22
event_start = threading.Event()
event_stop = threading.Event()

def start():
    logger.info("set event start...")
    # bms_interface.send_ctrl_cmd('1')
    event_start.set()

def stop():
    event_stop.set()
    logger.info("set event stop...")
    # bms_interface.send_ctrl_cmd('2')

# def reboot():
#     logger.info("send bms ctrl cmd reboot...")
#     bms_interface.send_ctrl_cmd('3')
#     logger.info("bms rebooted...")

image_proxy = xmlrpclib.ServerProxy("http://192.168.24.108:5001/")
image_proxy_lock = xmlrpclib.ServerProxy("http://192.168.24.108:5001/")

##scan_and_lock
def get_td():
    print '11'
    td =image_proxy_lock.get_td()
    print td
    return td

def get_enemy_coord():
    print '22'
    return image_proxy_lock.get_enemy_coord()

def get_Index():
    print '33'
    return image_proxy_lock.get_Index()


def get_Ropt():

    return image_proxy_lock.get_Ropt()

def get_Rpi():

    return image_proxy_lock.get_Rpi()

def get_Rtr():

    return image_proxy_lock.get_Rtr()

##fly

def get_miss_clock():

    return image_proxy.get_miss_clock()
#
# def get_Index():
#     # print '33'
#     return image_proxy.get_Index()
#
#
# def get_Ropt():
#
#     return image_proxy.get_Ropt()
#
# def get_Rpi():
#
#     return image_proxy.get_Rpi()
#
# def get_Rtr():
#
#     return image_proxy.get_Rtr()




# flag_entrance = False
flag_break = False
event_entrance = threading.Event()

lock_break = threading.Lock()
lock_entrance = threading.Lock()

def set_flag_break(action):
    global flag_break
    lock_break.acquire()
    flag_break = action
    lock_break.release()

def get_flag_entrance():
    # return flag_entrance
    event_entrance.wait()

def down(t):
    # global jiali
    # if jiali == 0:
    #     bms_interface.sendto("2004,-1")
    #     jiali = 1
    # if parsejson_targetscan()["radar_on"] == True:
    #     print "关雷达"
    #     LockonInterface.sendto("106")
    #     LockonInterface.sendto("86")
        # time.sleep(0.2)
    speedup(430)
    time.sleep(10)
    # LockonInterface.sendto("358")
    t_ganrao = time.time()

    t_duodaodan = time.time()
    bms_interface.sendto("y:25000")

    while (time.time() - t_duodaodan) < 3:
        speedup(430)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "半筋斗翻转"
        keep_roll(-math.pi)
        # time.sleep(0.05)

    t_duodaodan = time.time()
    while (time.time() - t_duodaodan) < 3:
        speedup(430)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "半筋斗翻转"
        # time.sleep(0.05)
    while parsejson_pitch() < 0:
        speedup(430)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "半筋斗翻转"
        # time.sleep(0.05)

    t_duodaodan = time.time()
    # print "筋斗完毕"

    while (time.time() - t_duodaodan) < t:
        speedup(430)
        keep_roll(0)
        keep_speed_vector(0)
        # keep_altrad(5000)
        # time.sleep(0.05)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "下降到高度1500米"

def up(t):
    # global jiali
    # if jiali == 0:
    #     bms_interface.sendto("2004,-1")
    #     jiali = 1
    if parsejson_targetscan()["radar_on"] == True:
        print "关雷达"
        bms_interface.sendto("106")
        bms_interface.sendto("86")
        time.sleep(0.2)

    bms_interface.sendto("358")
    t_ganrao = time.time()

    t_duodaodan = time.time()
    bms_interface.sendto("2001,0.3")
    while (time.time() - t_duodaodan) < 2:
        speedup(250)
        keep_roll(0)
        if (time.time() - t_ganrao) > 1:
            bms_interface.sendto("358")
            t_ganrao = time.time()
            print "向上翻转"
        time.sleep(0.05)
    while parsejson_pitch() > 0.1:
        speedup(250)
        if (time.time() - t_ganrao) > 1:
            bms_interface.sendto("358")
            t_ganrao = time.time()
            print "向上翻转"
        time.sleep(0.05)

    t_duodaodan = time.time()
    print "翻转完毕"

    if parsejson_targetscan()["radar_on"] == False:
        print "开雷达"
        bms_interface.sendto("106")
        bms_interface.sendto("86")
        time.sleep(0.2)

    while (time.time() - t_duodaodan) < t:
        speedup(250)
        keep_roll(0)
        keep_pitch(0)
        time.sleep(0.05)
        if (time.time() - t_ganrao) > 1:
            bms_interface.sendto("358")
            t_ganrao = time.time()
            print "转平"

def s_left(flag_break):
    # global jiali,flag_entrance
    # global jiali
    # if jiali == 0:
    #     bms_interface.sendto("2004,-1")
    #     jiali = 1
    # if parsejson_targetscan()["radar_on"] == True:
    #     print "关雷达"
    #     bms_interface.sendto("106")
    #     bms_interface.sendto("86")
    #     time.sleep(0.2)
    speedup(430)
    time.sleep(10)

    t_duodaodan = time.time()
    t_ganrao =time.time()

    while (time.time() - t_duodaodan) < 20:
        speedup(430)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "左转"
        keep_roll(-75*math.pi/180)   ###-80
        keep_speed_vector(10*math.pi/180)   ###8
        # keep_altbar(1500)
        # time.sleep(0.05)

    t_duodaodan = time.time()

    while (time.time() - t_duodaodan) < 1:
        speedup(430)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()

        keep_roll(0)
        keep_speed_vector(0)
        # keep_altbar(1500)
        # time.sleep(0.05)

    # lock_entrance.acquire()
    # flag_entrance = True
    # lock_entrance.release()
    # event_entrance.set()

    # while not flag_break:
    while (time.time() - t_duodaodan) < 5:
        speedup(430)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()

        keep_roll(0)
        keep_speed_vector(0)
        # keep_altbar(1500)
        # time.sleep(0.1)

def s_right(flag_break):
    # global jiali,flag_entrance
    # global jiali
    # if jiali == 0:
    #     bms_interface.sendto("2004,-1")
    #     jiali = 1
    # if parsejson_targetscan()["radar_on"] == True:
    #     print "关雷达"
    #     bms_interface.sendto("106")
    #     bms_interface.sendto("86")
    #     time.sleep(0.2)
    speedup(430)
    # bms_interface.sendto("z:0")
    t_duodaodan = time.time()
    t_ganrao =time.time()

    while (time.time() - t_duodaodan) < 20:
        speedup(430)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "右转"
        keep_roll(75 * math.pi / 180)   #80
        keep_speed_vector(10 * math.pi / 180)   #8
        # time.sleep(0.05)

    t_duodaodan = time.time()

    while (time.time() - t_duodaodan) < 1:
        speedup(430)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()

        keep_roll(0)
        keep_speed_vector(0)
        # time.sleep(0.05)

    # lock_entrance.acquire()
    # flag_entrance = True
    # lock_entrance.release()
    event_entrance.set()

    # while not flag_break:
    while (time.time() - t_duodaodan) < 5:
        speedup(430)
        if (time.time() - t_ganrao) > 1:
            # bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "下降到高度1500米"
        keep_roll(0)
        keep_speed_vector(0)
        # keep_altbar(1500)
        # time.sleep(0.1)


def off_set(yaw,va):
    #敌机在我机位置：delta_yaw = (x - 225)/225.0*60，负在左，正在右
    #if delta_yaw < 0:向右偏置50-abs(delta_yaw)
    #else:向左偏置50-abs(delta_yaw)
    if random.randint(0, 9) < 5:
        print "向右偏置"
        target_yaw = yaw + 5*math.pi/18
        if target_yaw > 2*math.pi:
            target_yaw = target_yaw -2*math.pi
        current_yaw = parsejson_yaw()
        e_yaw = target_yaw - current_yaw
        if e_yaw < -math.pi:
            e_yaw = e_yaw + 2*math.pi
        while e_yaw > 0:
            keep_roll(math.pi/3)
            # keep_speed_vector(va)
            current_yaw = parsejson_yaw()
            e_yaw = target_yaw - current_yaw
            if e_yaw < -math.pi:
                e_yaw = e_yaw + 2 * math.pi
    else:
        print "向左偏置"
        target_yaw = yaw - 5*math.pi/18
        if target_yaw < 0:
            target_yaw = target_yaw + 2 * math.pi
        current_yaw = parsejson_yaw()
        e_yaw = target_yaw - current_yaw
        if e_yaw > math.pi:
            e_yaw = e_yaw - 2 * math.pi
        while e_yaw < 0:
            keep_roll(-math.pi/3)
            # keep_speed_vector(va)
            current_yaw = parsejson_yaw()
            e_yaw = target_yaw - current_yaw
            if e_yaw > math.pi:
                e_yaw = e_yaw - 2 * math.pi

    t=time.time()
    print "转平"
    while (time.time() - t) < 3:
        keep_roll(0)
        keep_speed_vector(va)
        # time.sleep(0.05)
    print "发弹"
    # bms_interface.sendto("350")
    # time.sleep(1)

def turn_to_angle1(angle,t):
    # global jiali
    # if jiali == 0:
    #     bms_interface.sendto("2004,-1")
    #     jiali = 1
    if parsejson_targetscan()["radar_on"] == True:
        print "关雷达"
        bms_interface.sendto("106")
        bms_interface.sendto("86")
        time.sleep(0.2)

    t_duodaodan = time.time()
    t_ganrao =time.time()

    while (time.time() - t_duodaodan) < 25:
        speedup(250)
        if (time.time() - t_ganrao) > 1:
            bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "左转"
        keep_yaw_Va(angle,0)
        time.sleep(0.05)

    t_duodaodan = time.time()
    while (time.time() - t_duodaodan) < t:
        speedup(250)
        if (time.time() - t_ganrao) > 1:
            bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "下降到高度1500米"
        keep_roll(0)
        keep_altbar(1500)
        time.sleep(0.1)

def turn_to_angle2(angle,flag_break):
    # global jiali,flag_entrance
    # global jiali
    # if jiali == 0:
    #     bms_interface.sendto("2004,-1")
    #     jiali = 1
    if parsejson_targetscan()["radar_on"] == True:
        print "关雷达"
        bms_interface.sendto("106")
        bms_interface.sendto("86")
        time.sleep(0.2)

    t_duodaodan = time.time()
    t_ganrao =time.time()

    while (time.time() - t_duodaodan) < 25:
        speedup(250)
        if (time.time() - t_ganrao) > 1:
            bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "左转"
        keep_yaw_Va(angle,0)
        time.sleep(0.05)

    t_duodaodan = time.time()

    while (time.time() - t_duodaodan) < 1:
        speedup(250)
        if (time.time() - t_ganrao) > 1:
            bms_interface.sendto("358")
            t_ganrao = time.time()

        keep_roll(0)
        keep_altbar(1500)
        time.sleep(0.05)

    # lock_entrance.acquire()
    # flag_entrance = True
    # lock_entrance.release()
    event_entrance.set()

    while not flag_break:
        speedup(250)
        if (time.time() - t_ganrao) > 1:
            bms_interface.sendto("358")
            t_ganrao = time.time()
            # print "下降到高度1500米"
        keep_roll(0)
        keep_altbar(1500)
        time.sleep(0.05)

def down_S():
    if parsejson_altRad() > 3000:
        down(20)
    else:
        s_left(10)
        s_left(10)
    s_left(10)

def s_down():
    s_left(8)
    if parsejson_altRad() > 3000:
        down(10)
    else:
        s_left(10)
        s_left(10)
def reverse_direction():
    if parsejson_altRad() > 3000:
        down(12)
    else:
        s_right(10)
        s_right(10)

bms_interface = BmsInterface.BmsIf()

def joystick_initialization():
    logger.warn("fly initialization...")
    bms_interface.sendto("x:16383")
    time.sleep(0.5)
    bms_interface.sendto("y:16383")
    time.sleep(0.5)
    bms_interface.sendto("z:32766")
    time.sleep(0.5)


def fly_initialization():
    # bms_interface.sendto("K:46")    # Toggle exterior lighting
    # bms_interface.sendto("K:398")   # View: HUD only
    bms_interface.sendto("K:329")   # Switch to next waypoint(matchplay mode, remove waypoint symbol on LMFD)
    # time.sleep(0.1)
    bms_interface.sendto("K:158")
    bms_interface.sendto("K:171")
    # time.sleep(0.1)
    bms_interface.sendto("K:171")
    bms_interface.sendto("K:171")
    bms_interface.sendto("K:158")
    # time.sleep(0.1)
    bms_interface.sendto("K:164")   # LMFD: OSB11--cleanse LMFD
    bms_interface.sendto("K:182")   # clear LMFD field
    bms_interface.sendto("K:288")
    bms_interface.sendto("K:250")
    bms_interface.sendto("K:250")



lockcommand=threading.Lock()
Input =0
yaw =0.00
pitch= 0.00
def set_command():
    global Input, roll, pitch, yaw, lockcommand, va, high,t
    time.sleep(2)
    while 1:
        # flag = input("输入标识1或2：")
        # a = input("输入横滚角（-180 - 180）：")
        # c = input("输入偏航角（-180 - 180）：")
        # d = input("输入俯仰角（-90 - 90）：")
        # high = input("输入保持高度（10000-16000）：")
        # t = input("输入平飞时间：")


        # Input = 0
        lockcommand.acquire()
        # print speed_vector()
        # roll = (a / 180.0) * math.pi
        # print 'roll:', 180 * parsejson_bank() / math.pi
        # yaw = (c / 180.0) * math.pi
        # print 'yaw:', 180 * parsejson_yaw() / math.pi
        # va = (d / 180.0) * math.pi
        # print 'va:', 180 * speed_vector() / math.pi
        # print '速度：', parsejson_speed()
        # print '实际高度:',parsejson_altRad()
        # print '微分:', delta_e
        lockcommand.release()
        Input = 1

##随机飞行
def random_fly():
    while True:
        logger.warn("...waiting for start event...")
        event_start.wait()
        time.sleep(12)
        logger.warn("...start an episode...")
        # bms_interface.sendto("K:398")
        init_time = time.time()
        time.sleep(2)
        while (time.time() - init_time) < 10:
            speedup(430)
            keep_roll(0)
            keep_speed_vector(0)
        init_high = random.normalvariate(13000,1250)
        random_yaw = random.randint(-45, 45)
        init_yaw = parsejson_yaw() + (random_yaw*math.pi/180)
        while abs(init_yaw - parsejson_yaw()) > 0.1*math.pi/ 180:
            speedup(430)
            keep_yaw_Va(init_yaw,0.1)
        init_time = time.time()
        while (time.time() - init_time) < 10:
            speedup(430)
            keep_yaw_Va(init_yaw, 0)
        while True:
            speedup(430)
            keep_roll(0)
            keep_altrad(init_high)
            if event_stop.is_set():
                logger.warn("...stop an episode...")
                event_stop.clear()
                break

def keep_levelflight():
    global Input,yaw, pitch
    while True:
        event_start.wait()
        logger.warn("...start an episode...")
        while True:
            speedup(430)
            keep_roll(0)
            keep_altrad(parsejson_altRad())
            if event_stop.is_set():
                logger.warn("...stop an episode...")
                event_stop.clear()
                break
            # bms_interface.sendto("x:16383.5")
            # bms_interface.sendto("y:16383.5")

def fly_test():
    global Input,pitch
    yaw = parsejson_yaw()
    nose_up_flag = 0
    # fire_flag = 0
    # thread_console = threading.Thread(target = set_command)
    # thread_console.start()
    while 1:
        while 1:
            # print '11'
            # lockcommand.acquire()
            speedup(430)
            # UdpClient.sendto("z:0")
            # print '速度：', parsejson_speed()
            # keep_pitch(pitch)
            # keep_yaw_Va(yaw,va)
            # print pitch
            # keep_roll(roll)
            # keep_speed_vector(va)
            # keep_altrad(high)
            # spiral(roll, va)
            # down(10)
            # s_left(0)
            # s_right(0)
            # keep_levelflight()
            miss_clock_digit, fcr_nose_up = get_miss_clock()
            if (fcr_nose_up is not None):
                nose_up_flag = 1
                nose_up = math.pi*int(float(fcr_nose_up))/180.0
                print 'nose_up: ', nose_up
                keep_speed_vector(nose_up)
                print 'speed_vector: ', speed_vector()
            else:
                if (nose_up_flag == 1):
                    # print 'nose_up_flag == 1'
                    keep_speed_vector(nose_up)
                else:
                    # print 'fly1112344'
                    keep_roll(0)
                    keep_yaw_Va(yaw, 0)
                    keep_speed_vector(0)
            if fire_flag == 1:
                # print 'fire1241'
                keep_roll(0)
                keep_yaw_Va(yaw, 0)
                keep_speed_vector(0)
                nose_up_flag = 0

            if miss_clock_digit is not None:
                keep_roll(0)
                keep_yaw_Va(yaw, 0.0)
                keep_speed_vector(0)
            # keep_altrad(14000)
            # scan_and_lock()


def initFlyCtrl():
    t2 = threading.Thread(target=fly_test)
    t2.start()

def lock_and_fire():
    global Input
    fire_count=0
    t_fire = time.time()
    while 1:
        while Input:
            time.sleep(0.05)
            if parsejson_targetscan()["radar_on"] == False:
                print "开雷达"
                bms_interface.sendto("106")
                bms_interface.sendto("86")
                time.sleep(0.2)

            target_scan = parsejson_target()
            target_lock = parsejson_lockedtarget()
            #锁定
            if target_scan != [] and target_lock==[]:
                scan_and_lock()
                time.sleep(0.1)
            #发弹
            if target_lock != []:
                if target_lock[0]["target"]['distance'] < target_lock[0]['DLZ']['RPI']:
                    if (fire_count < 2) and ((time.time() - t_fire) > 2):
                        fire_count = fire_count + 1
                        print "fire ", fire_count
                        bms_interface.sendto("84")
                        t_fire = time.time()
            else:
                fire_count = 0

def initLock_and_fire():
    t4 = threading.Thread(target=lock_and_fire)
    t4.start()


def missile_count():
    temp = parsejson_loadinfor()
    if temp is not None:
        loadinfor = temp['Stations']
        count=0
        for i in loadinfor:
            if i['weapon']['level3']==7:
                count=count +1
        return count
    else:
        return None



def fly_from_ground():
    global jiali
    jinyi=0
    qiluojia=0
    #放襟翼
    bms_interface.sendto("145")
    time.sleep(0.5)

    #加速
    if jiali == 0:
        bms_interface.sendto("2004,-1")
        jiali = 1

    t=time.time()
    while (time.time() - t) < 30:
        alt=parsejson_altRad()

        time.sleep(0.05)
        # 高度大于20收起落架
        if (alt > 10) and (qiluojia==0):
            print "收起落架"
            bms_interface.sendto("430")
            qiluojia=1
            t_qiluojia=time.time()
            # time.sleep(0.05)
        if qiluojia==0:
            keep_pitch(0.3)
        if qiluojia==1:
            if (time.time()-t_qiluojia)< 5:
                keep_pitch(0.3)
            else:
                keep_pitch(0.6)

        # 高度大于100收襟翼
        if (alt > 100) and (jinyi==0):
            print "收襟翼"
            bms_interface.sendto("146")
            jinyi=1
            # time.sleep(0.05)

    # while parsejson_altBar() < 1500:
    #     keep_yaw_pitch(math.pi/4,0.2)
    #     time.sleep(0.05)
    while parsejson_altBar() < 3000:
        keep_yaw_Va(math.pi/4,0.4)
        time.sleep(0.05)



e_groundyaw_last=0
t_groundyaw=time.time()
def keep_groundyaw(yaw):
    global t_groundyaw, e_groundyaw_last
    e_yaw = yaw - parsejson_yaw()
    if e_yaw > math.pi:
        e_yaw = e_yaw - 2 * math.pi
    if e_yaw < -math.pi:
        e_yaw = e_yaw + 2 * math.pi

    if (time.time() - t_groundyaw) > 0.05:
        a = 7 * e_yaw+(e_yaw-e_groundyaw_last)
        if a > 1:
            a = 1
        if a < -1:
            a = -1
        command = "2003" + "," + str(a)
        bms_interface.sendto(command)
        e_groundyaw_last = e_yaw
        t_groundyaw = time.time()


def drive_to_runway():
    #左转
    bms_interface.sendto("2003,-1")
    #启动
    print "启动"
    bms_interface.sendto("2004,-0.1")
    time.sleep(2)
    bms_interface.sendto("2004,0")

    t_print = time.time()
    while parsejson_yaw()>4.486:
        if (time.time()-t_print) > 1:
            # print"当前航向角", 180*parsejson_yaw()/3.14
            print "转弯"
            t_print = time.time()

    #加油
    bms_interface.sendto("2004,-0.6")
    shouyou1=0
    while parsejson_selfinfor()['Position']['z'] > 635000:
        keep_groundyaw(4.486)
        time.sleep(0.05)
        if (parsejson_speed()>50) and (shouyou1==0):
            print "收油"
            bms_interface.sendto("2004,1")
            shouyou1=1
        if (time.time()-t_print) > 1:
            print "第一段路"
            print "速度",parsejson_speed()
            t_print = time.time()


    bms_interface.sendto("2003,-1")

    while parsejson_yaw()>4.368:
        if (time.time()-t_print) > 1:
            # print"当前航向角", 180*parsejson_yaw()/3.14
            print"转弯"
            t_print = time.time()

    # print "启动"
    # bms_interface.sendto("2004,-0.1")
    # time.sleep(2)
    # bms_interface.sendto("2004,0")



    print "第二段路"#更换电脑后有可能出现转弯过早或过晚：过早调小，过晚调大
    while parsejson_selfinfor()['Position']['z'] > 634858:
        # 634858
        keep_groundyaw(4.368)
        time.sleep(0.05)
        if (time.time()-t_print) > 1:
            print "第二段路"
            print "速度", parsejson_speed()
            print "位置", parsejson_selfinfor()['Position']['z']
            t_print = time.time()

    print "减速"
    bms_interface.sendto("74")
    while parsejson_speed()>10:
        if (time.time()-t_print) > 1:
            print "速度", parsejson_speed()
            t_print = time.time()
    bms_interface.sendto("75")

    bms_interface.sendto("2003,1")
    while parsejson_yaw()< 5.8:
        if (time.time()-t_print) > 1:
            # print"当前航向角", 180*parsejson_yaw()/3.14
            print"转弯"
            t_print = time.time()

    print "加速"
    bms_interface.sendto("2004,-0.5")
    shouyou2=0
    print "第三段路"
    while parsejson_selfinfor()['Position']['z'] > 634562:
        # 634562
        keep_groundyaw(5.8)
        time.sleep(0.05)
        if (parsejson_speed()>10) and (shouyou2==0):
            print "收油"
            bms_interface.sendto("2004,1")
            shouyou2=1
        if (time.time()-t_print) > 1:
            print "第三段路"
            print "速度", parsejson_speed()
            print "位置", parsejson_selfinfor()['Position']['z']
            t_print = time.time()

    bms_interface.sendto("2003,1")
    e=1
    while e > 0:
        e=1.2280-parsejson_yaw()
        if e < -math.pi:
            e=e+2*math.pi
        if (time.time() - t_print) > 1:
            print"转弯"
            t_print = time.time()

    t=time.time()
    while (time.time()-t)<2:
        keep_groundyaw(1.2280)
        time.sleep(0.05)
        if (time.time()-t_print) > 1:
            print "第四段路"
            print "速度", parsejson_speed()
            print "位置", parsejson_selfinfor()['Position']['z']
            t_print = time.time()

    print "制动"
    bms_interface.sendto("74")
    bms_interface.sendto("2004,1")
    time.sleep(2)
    bms_interface.sendto("75")


def back_and_landing():
    print "敌机坠毁，返航"

    if parsejson_targetscan()["radar_on"] == True:
        print "关雷达"
        bms_interface.sendto("106")
        bms_interface.sendto("86")
        time.sleep(0.2)
    print "关加力"
    bms_interface.sendto("2004,0")

    tar_x = -318158.1875
    tar_y = 2000
    tar_z = 635724.9375 - 13400

    my_position = parsejson_selfinfor()['Position']
    dis = math.sqrt(
        (tar_x - my_position['x']) ** 2 + (tar_y - my_position['y']) ** 2 + (
            tar_z - my_position['z']) ** 2)

    while dis > 5000:

        my_position = parsejson_selfinfor()['Position']
        dis = math.sqrt(
            (tar_x - my_position['x']) ** 2 + (tar_y - my_position['y']) ** 2 + (
                tar_z - my_position['z']) ** 2)
        delta_h = tar_y - my_position['y']
        pitch_command = math.asin(delta_h / dis)
        yaw_command = math.pi / 2 - math.atan2((tar_x - my_position['x']),
                                               (tar_z - my_position['z']))
        if yaw_command > math.pi:
            yaw_command = yaw_command - 2 * math.pi
        if yaw_command < -math.pi:
            yaw_command = yaw_command + 2 * math.pi

        if yaw_command < 0:
            yaw_command = yaw_command + 2 * math.pi

        # print "yaw_command",yaw_command
        # print "pitch_command", pitch_command
        keep_yaw_Va(yaw_command, pitch_command)
        time.sleep(0.05)



        # if dis > 10000:
        #     speedup(310)
        # else:
        #     speedup(100)

    # 自动巡航返航

    print"开始自动着陆"
    bms_interface.sendto("105")  # 切换导航模式
    time.sleep(1)
    bms_interface.sendto("62")  # 自动驾驶
    time.sleep(1)

    qiluojia = 0
    alt = parsejson_altRad()
    while alt > 3:
        alt = parsejson_altRad()
        print "alt =", alt
        if alt < 300 and qiluojia == 0:
            print "放起落架"
            bms_interface.sendto("431")
            qiluojia = 1
        if alt < 4:
            time.sleep(1)
            bms_interface.sendto("74")
            time.sleep(1)
        time.sleep(1)
    time.sleep(15)
    print "关闭引擎"
    bms_interface.sendto("310")
    time.sleep(1)
    bms_interface.sendto("313")
    time.sleep(1)
    bms_interface.sendto("314")
    time.sleep(1)
    bms_interface.sendto("71")

def combat_test():
    global jiali
    while 1:
        t_print = time.time()
        t_fire = 0
        shijiao = 0
        flag_done = False

        a = input("输入开始指令：")
        # while 1:
        #     print parsejson_target()
        #     time.sleep(1)

        t_finish = time.time()
        if shijiao==0:
            bms_interface.sendto("8")
            bms_interface.sendto("36")
            bms_interface.sendto("336")
            time.sleep(1.3)
            bms_interface.sendto("337")
            shijiao=1
        # drive_to_runway()
        # fly_from_ground()

        fire_count = 0
        fire_flag = 0
        detect = 0
        shoot_dis = 100000
        roll_command_last=1.2

        enemy_position_last=[]
        missile_shoot_time = time.time()
        waittime = 0

        if shijiao==1:
            bms_interface.sendto("7")
            bms_interface.sendto("36")
            shijiao=0


        while 1:
            # (time.time() - get_datatime()) < 2:
            # (time.time() - get_datatime()) < 2:
            time.sleep(0.05)

            flag = 0

            #####采基本数据###
            # 从预警系统拿敌机信息
            enemy_infor = parsejson_enermy()
            enemy_detail = parsejson_enermy_detail()
            enemy_yaw = []
            enemy_position = []
            #print(enemy_detail)
            for i in enemy_detail:
                if i['Type']['level3'] == 1:
                    enemy_yaw = i['Heading']
                    enemy_position = i['Position']
                    enemy_position_last=i['Position']
                    flag = (flag or 1)
                else:
                    flag = (flag or 0)

            ##从我机雷达系统拿敌机信息
            target_scan= parsejson_target()
            target_lock = parsejson_lockedtarget()
            if target_scan != []:
                enemy_position = target_scan[0]['position']['p']
                enemy_position_last = target_scan[0]['position']['p']



            # 拿我机信息
            my_position = parsejson_selfinfor()['Position']
            my_yaw = parsejson_yaw()
            my_altbar = parsejson_altBar()
            my_altrad = parsejson_altRad()

            # 计算与敌机距离,高度差，并计算相应的yaw和pitch
            if enemy_position != []:
                reach_taget=0
                # 计算与敌机距离,高度差，并计算相应的yaw和pitch
                dis = math.sqrt(
                    (enemy_position['x'] - my_position['x']) ** 2 + (enemy_position['y'] - my_position['y']) ** 2 + (
                        enemy_position['z'] - my_position['z']) ** 2)
                delta_h = enemy_position['y'] - my_position['y']
                pitch_command = math.asin(delta_h/dis)
                yaw_command = math.pi / 2 - math.atan2((enemy_position['x'] - my_position['x']),
                                                       (enemy_position['z'] - my_position['z']))
                if yaw_command > math.pi:
                    yaw_command = yaw_command - 2 * math.pi
                if yaw_command < -math.pi:
                    yaw_command = yaw_command + 2 * math.pi

                if yaw_command < 0:
                    yaw_command = yaw_command + 2 * math.pi

                # e_yaw = yaw_command - yaw_command_last
                # if e_yaw > math.pi:
                #     e_yaw = e_yaw - 2 * math.pi
                # if e_yaw < -math.pi:
                #     e_yaw = e_yaw + 2 * math.pi
                # if abs(e_yaw) > 0.15:
                #     yaw_command_last = yaw_command

            # 拿预警信息
            # print enemy_detail
            signal = 0
            # missile_dis = 100000
            missile_angle = 0
            # print enemy_detail
            for i in enemy_detail:
                if i['Type']['level3'] == 7:
                    print  "有导弹"
                    print enemy_detail
                    signal = 1
                    missile_position = i['Position']
                    # dis_temp = math.sqrt(
                    #     (missile_position['x'] - my_position['x']) ** 2 + (
                    #         missile_position['y'] - my_position['y']) ** 2 + (
                    #         missile_position['z'] - my_position['z']) ** 2)
                    # if dis_temp < missile_dis:
                    #     missile_dis = dis_temp

                    missile_angle = math.pi / 2 - math.atan2((missile_position['x'] - my_position['x']),
                                                           (missile_position['z'] - my_position['z']))
                    if missile_angle > math.pi:
                        missile_angle = missile_angle - 2 * math.pi
                    if missile_angle < -math.pi:
                        missile_angle = missile_angle + 2 * math.pi

                    if missile_angle < 0:
                        missile_angle = missile_angle + 2 * math.pi


            if detect == 0:
                # print enemy_infor
                for i in enemy_infor:
                    if i['Type']['level3'] == 1:
                        #如果被敌机发射导弹，记录下两机距离
                        if i['SignalType'] == 'missile_radio_guided':
                            shoot_dis = dis
                            if shoot_dis < 40000:
                                missile_shoot_time = time.time()
                                waittime = 25 * (shoot_dis - 15000) / 25000
                            detect = 1
                            print "导弹发射距离",shoot_dis

            ###逻辑开始###
            # 如果有导弹威胁，则优先躲导弹
            # or ((detect == 1) and ((time.time() - missile_shoot_time) > 6))
            if ((signal == 1) and (fire_flag == 0 or (time.time() - t_finish) > 25)) or ((shoot_dis < 40000) and ((time.time() - missile_shoot_time) > waittime)):
                if (shoot_dis < 40000) and ((time.time() - missile_shoot_time) > waittime):
                    print "因倒计时结束进入"
                else:
                    print "因收到导弹来袭信号进入"
                fire_flag = fire_count

                if shijiao == 0:
                    bms_interface.sendto("8")
                    shijiao = 1
                reverse_angle = 0
                # 躲导弹机动之前如果能发弹就先打一颗再跑
                if target_lock != []:
                    if target_lock[0]["target"]['distance'] < target_lock[0]['DLZ']['RPI']:
                        fire_count = fire_count +1
                        print "fire", fire_count
                        bms_interface.sendto("84")
                        time.sleep(1)
                # fire_count = 0
                print "躲导弹"

                e_angle = my_yaw - yaw_command
                if e_angle > math.pi:
                    e_angle = e_angle - 2 * math.pi
                if e_angle < -math.pi:
                    e_angle = e_angle + 2 * math.pi
                reverse_angle = yaw_command + math.pi

                if reverse_angle > 2 * math.pi:
                    reverse_angle = reverse_angle - 2 * math.pi

                # t_gaojing = time.time()
                # print "告警时间", t_gaojing

                # if shoot_dis<30000:
                #     e_angle = my_yaw - yaw_command
                #     if e_angle > math.pi:
                #         e_angle = e_angle - 2 * math.pi
                #     if e_angle < -math.pi:
                #         e_angle = e_angle + 2 * math.pi
                #     reverse_angle = yaw_command + math.pi
                #     if reverse_angle > 2*math.pi:
                #         reverse_angle = reverse_angle - 2*math.pi
                # else:
                #     e_angle = my_yaw-missile_angle
                #     if e_angle > math.pi:
                #         e_angle = e_angle - 2 * math.pi
                #     if e_angle < -math.pi:
                #         e_angle = e_angle + 2 * math.pi
                #
                #     reverse_angle = missile_angle + math.pi
                #     if reverse_angle > 2 * math.pi:
                #         reverse_angle = reverse_angle - 2 * math.pi
                #
                #
                # if shoot_dis < 30000:
                #     missile_angle = yaw_command
                #
                # print "导弹角度",missile_angle*180/3.14
                #
                # if abs(e_angle)< (math.pi/2):
                #     if e_angle> 0:
                #         angle1 = missile_angle + math.pi/2
                #     else:
                #         angle1 = missile_angle - math.pi/2
                #     if angle1 > 2*math.pi:
                #         angle1 = angle1 - 2 * math.pi
                #     if angle1 < 0:
                #         angle1 = angle1 + 2 * math.pi

                print "离地面高度",my_altrad
                # print e_angle
                #如果导弹在前方，则下转身之后逃离
                if (abs(e_angle)<(math.pi/2)) and (my_altrad>2800):
                    down(8)
                    print "当前速度",parsejson_speed()
                    if random.randint(0,9) < 5:
                        # s_right(5)
                        # s_right(5)
                        # s_right(2)
                        # roll_command_last = 1.2

                        ##或者
                        s_right(flag_break)
                        up(3)
                        roll_command_last = -1.2
                    else:
                        # s_left(5)
                        # s_left(5)
                        # s_left(2)
                        # roll_command_last = -1.2

                        ##或者
                        s_left(flag_break)
                        up(3)
                        roll_command_last = 1.2

                #否则直接转向导弹相反方向逃离
                else:
                        # print "转向垂直于导弹的方向"
                        # print "垂直角度", angle1 * 180 / 3.14
                        # turn_to_angle1(angle1, 0)

                        print "转向导弹相反方向"
                        print "反向角度",reverse_angle*180/3.14
                        turn_to_angle2(reverse_angle, flag_break)

                        # up(3)
                        # s_left(3)
                        # s_right(3)

                t_finish=time.time()

                shoot_dis = 100000
                detect = 0 #暂时没用

                if shijiao == 1:
                    bms_interface.sendto("7")
                    shijiao = 0

            # 如果没有导弹威胁，则执行。。。
            else:
                speedup(250)
                ##如果已锁定敌机，则追踪敌机并伺机发弹
                if target_lock != []:

                    if (time.time() - t_print) > 2:
                        t_print = time.time()
                        print '追踪敌机，伺机发弹'
                        print "target_dis",target_lock[0]["target"]['distance']

                    yaw_error = yaw_command - my_yaw
                    if yaw_error > math.pi:
                        yaw_error = yaw_error - 2 * math.pi
                    if yaw_error < -math.pi:
                        yaw_error = yaw_error + 2 * math.pi

                    roll_command = 5 * yaw_error
                    if roll_command > 0.8:
                        roll_command = 0.8
                    if roll_command < -0.8:
                        roll_command = -0.8

                    keep_roll(roll_command)
                    # if detect==1:
                    #     if (time.time() - missile_shoot_time) < 50:
                    #         if pitch_command<0:
                    #             pitch_command=0
                    #     else:
                    #         detect=0
                    # if my_altrad< 3500:
                    #     if pitch_command < 0:
                    #         pitch_command = 0

                    #当飞机高度较低时，为了留出机动空间，不能跟敌机往下走，需保持一定高度
                    if (my_altbar<3600) and (pitch_command < 0.5):
                        keep_altbar(3500)
                    else:
                        keep_pitch(pitch_command)


                    if target_lock[0]["target"]['distance']<target_lock[0]['DLZ']['RPI']:
                        # and (target_lock[0]["target"]['distance'] < 40000)
                        if fire_count == 0:
                            fire_count=fire_count+1
                            print "fire ", fire_count
                            print target_lock[0]["target"]['distance']
                            bms_interface.sendto("84")
                            if shijiao == 0:
                                bms_interface.sendto("8")
                                shijiao = 1
                            t_fire = time.time()

                        else:
                            #15公里外隔20s发一颗
                            if target_lock[0]["target"]['distance']>15000:
                                if (time.time()-t_fire)>20:
                                    if fire_count<1:
                                        fire_count = fire_count + 1
                                        print "fire ", fire_count
                                        print target_lock[0]["target"]['distance']
                                        bms_interface.sendto("84")
                                        if shijiao == 0:
                                            bms_interface.sendto("8")
                                            shijiao = 1
                                        t_fire = time.time()
                            #15公里内10秒发一颗
                            else:
                                if (time.time()-t_fire)>10:
                                    if (fire_count<3) or (target_lock[0]["target"]['distance']<10000):
                                        fire_count = fire_count + 1
                                        print "fire ", fire_count
                                        print target_lock[0]["target"]['distance']
                                        bms_interface.sendto("84")
                                        if shijiao == 0:
                                            bms_interface.sendto("8")
                                            shijiao = 1
                                        t_fire = time.time()

                #如果未锁定敌机，则执行...
                else:
                    if shijiao == 1:
                        bms_interface.sendto("7")
                        shijiao = 0
                    fire_count=0
                    #如果扫描到敌机，则保持追踪并开始锁定
                    if target_scan != []:
                        yaw_error = yaw_command - my_yaw
                        if yaw_error > math.pi:
                            yaw_error = yaw_error - 2 * math.pi
                        if yaw_error < -math.pi:
                            yaw_error = yaw_error + 2 * math.pi

                        roll_command = 5 * yaw_error
                        if roll_command > 0.8:
                            roll_command = 0.8
                        if roll_command < -0.8:
                            roll_command = -0.8

                        keep_roll(roll_command)
                        keep_pitch(pitch_command)

                        scan_and_lock()
                        time.sleep(0.1)
                        if (time.time() - t_print) > 2:
                            t_print = time.time()
                            print '跟踪敌机，开始锁定'

                    # 如果未扫描到敌机，则执行。。。
                    else:
                        ##如果预警系统有敌机信号
                        if enemy_yaw != []:
                            #转向敌机
                            keep_yaw_Va(yaw_command, pitch_command)
                            #如果导弹在射程外，则关雷达潜伏
                            if dis > 100000:
                                if parsejson_targetscan()["radar_on"] == True:
                                    print "关雷达"
                                    bms_interface.sendto("106")
                                    bms_interface.sendto("86")
                                    time.sleep(0.2)
                                if (time.time() - t_print) > 2:
                                    t_print = time.time()
                                    print '转向敌机，潜伏'
                            # 如果导弹在射程内，则开雷达扫描
                            else:
                                if parsejson_targetscan()["radar_on"] == False:
                                    print "开雷达"
                                    bms_interface.sendto("106")
                                    bms_interface.sendto("86")
                                    time.sleep(0.2)
                                if (time.time() - t_print) > 2:
                                    t_print = time.time()
                                    print '转向敌机，搜索'

                        ##如果预警系统没有信号
                        else:
                            if parsejson_targetscan()["radar_on"] == False:
                                print "开雷达"
                                bms_interface.sendto("106")
                                bms_interface.sendto("86")
                                time.sleep(0.2)

                            ##如果记录了上一时刻敌机信息，则转向上一时刻的敌机位置
                            if enemy_position_last != []:
                                dis = math.sqrt(
                                    (enemy_position_last['x'] - my_position['x']) ** 2 + (
                                        enemy_position_last['y'] - my_position['y']) ** 2 + (
                                        enemy_position_last['z'] - my_position['z']) ** 2)
                                yaw_command = math.pi / 2 - math.atan2((enemy_position_last['x'] - my_position['x']),
                                                                       (enemy_position_last['z'] - my_position['z']))
                                if yaw_command > math.pi:
                                    yaw_command = yaw_command - 2 * math.pi
                                if yaw_command < -math.pi:
                                    yaw_command = yaw_command + 2 * math.pi

                                if yaw_command < 0:
                                    yaw_command = yaw_command + 2 * math.pi

                                yaw_error = yaw_command - my_yaw
                                if yaw_error > math.pi:
                                    yaw_error = yaw_error - 2 * math.pi
                                if yaw_error < -math.pi:
                                    yaw_error = yaw_error + 2 * math.pi

                                # ##在敌机消失方向左右摇晃搜索
                                if yaw_error > 0:
                                    roll_command = 1.2
                                else:
                                    roll_command = -1.2

                                if abs(yaw_error) < 1.1:
                                    roll_command = roll_command_last
                                else:
                                    roll_command_last = roll_command

                                if dis > 5000:
                                    keep_roll(roll_command)
                                    if my_altbar>5000:
                                        keep_pitch(0)
                                    elif my_altbar>3500:
                                        keep_pitch(0.04)
                                    else:
                                        keep_pitch(0.15)
                                else:
                                    keep_altbar(1500)
                                    keep_roll(0)

                                if (time.time() - t_print) > 2:
                                    t_print = time.time()
                                    print '在敌机消失位置方向搜索'

                            # 如果刚开局没有信息，则保持平飞搜索
                            else:
                                keep_altbar(5000)
                                keep_roll(0)
                                if (time.time() - t_print) > 2:
                                    t_print = time.time()
                                    print '无敌机信号,平飞搜索'

    # print "退出，敌机信息",parsejson_enemyid()
    # if shijiao == 0:
    #     bms_interface.sendto("8")
    #     shijiao=1
    # back_and_landing()


def initCombat():
    t3 = threading.Thread(target=combat_test)
    t3.start()