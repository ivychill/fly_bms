#!/usr/bin/env python
# encoding: utf-8
'''
@author: qingyao.wang
@license: (C) Copyright 2017-2020  kuang-chi Corporation Limited.
@contact: qingyao.wang@kuang-chi.com
@file: flightbitdemo.py
@time: 2018-01-29 13:33
@desc:
'''

import sys,json,time
# sys.path.append("BmsInterface.py")
import BmsInterface
from enum import Enum
from my_config import *

class LightBits1(Enum):

        MasterCaution = 0x1  # Left eyebrow

        # Brow Lights
        TF        = 0x2   # Left eyebrow
        OXY_BROW  = 0x4   # repurposed for eyebrow OXY LOW (was OBS unused)
        EQUIP_HOT = 0x8   # Caution light; repurposed for cooling fault (was: not used)
        ONGROUND  = 0x10  # True if on ground: this is not a lamp bit!
        ENG_FIRE  = 0x20  # Right eyebrow; upper half of split face lamp
        CONFIG    = 0x40  # Stores config caution panel
        HYD       = 0x80  # Right eyebrow; see also OIL (this lamp is not split face)
        Flcs_ABCD = 0x100 # TEST panel FLCS channel lamps; repurposed was OIL (see HYD; that lamp is not split face)
        FLCS      = 0x200 # Right eyebrow; was called DUAL which matches block 25 30/32 and older 40/42
        CAN       = 0x400 # Right eyebrow
        T_L_CFG   = 0x800 # Right eyebrow

        # AOA Indexers
        AOAAbove  = 0x1000
        AOAOn     = 0x2000
        AOABelow  = 0x4000

        # Refuel/NWS
        RefuelRDY = 0x8000
        RefuelAR  = 0x10000
        RefuelDSC = 0x20000

        # Caution Lights
        FltControlSys = 0x40000
        LEFlaps       = 0x80000
        EngineFault   = 0x100000
        Overheat      = 0x200000
        FuelLow       = 0x400000
        Avionics      = 0x800000
        RadarAlt      = 0x1000000
        IFF           = 0x2000000
        ECM           = 0x4000000
        Hook          = 0x8000000
        NWSFail       = 0x10000000
        CabinPress    = 0x20000000

        AutoPilotOn   = 0x40000000  # TRUE if is AP on.  NB: This is not a lamp bit!
        TFR_STBY      = 0x80000000  # MISC panel; lower half of split face TFR lamp

        # Used with the MAL/IND light code to light up "everything"
        # please update this if you add/change bits!
        AllLampBitsOn     = 0xBFFFFFEF


class LightBits2(Enum):
    # Threat Warning Prime
    HandOff = 0x1
    Launch  = 0x2
    PriMode = 0x4
    Naval   = 0x8
    Unk     = 0x10
    TgtSep  = 0x20
    # EWS
    Go		= 0x40		# On and operating normally
    NoGo    = 0x80     # On but malfunction present
    Degr    = 0x100    # Status message: AUTO DEGR
    Rdy     = 0x200    # Status message: DISPENSE RDY
    ChaffLo = 0x400    # Bingo chaff quantity reached
    FlareLo = 0x800    # Bingo flare quantity reached

    # Aux Threat Warning
    AuxSrch = 0x1000
    AuxAct  = 0x2000
    AuxLow  = 0x4000
    AuxPwr  = 0x8000

    # ECM
    EcmPwr  = 0x10000
    EcmFail = 0x20000

    # Caution Lights
    FwdFuelLow = 0x40000
    AftFuelLow = 0x80000

    EPUOn      = 0x100000  # EPU panel; run light
    JFSOn      = 0x200000  # Eng Jet Start panel; run light

    # Caution panel
    SEC          = 0x400000
    OXY_LOW      = 0x800000
    PROBEHEAT    = 0x1000000
    SEAT_ARM     = 0x2000000
    BUC          = 0x4000000
    FUEL_OIL_HOT = 0x8000000
    ANTI_SKID    = 0x10000000

    TFR_ENGAGED  = 0x20000000  # MISC panel; upper half of split face TFR lamp
    GEARHANDLE   = 0x40000000  # Lamp in gear handle lights on fault or gear in motion
    ENGINE       = 0x80000000  # Lower half of right eyebrow ENG FIRE/ENGINE lamp

    # Used with the MAL/IND light code to light up "everything"
    # please update this if you add/change bits!
    AllLampBits2On = 0xFFFFF03F
    AllLampBits2OnExceptCarapace = AllLampBits2On ^ HandOff ^ Launch ^ PriMode ^ Naval ^ Unk ^ TgtSep ^ AuxSrch ^ AuxAct ^ AuxLow ^ AuxPwr



class LightBits3(Enum):
    # Elec panel
    FlcsPmg = 0x1
    MainGen = 0x2
    StbyGen = 0x4
    EpuGen  = 0x8
    EpuPmg  = 0x10
    ToFlcs  = 0x20
    FlcsRly = 0x40
    BatFail = 0x80

    # EPU panel
    Hydrazine = 0x100
    Air       = 0x200

    # Caution panel
    Elec_Fault = 0x400
    Lef_Fault  = 0x800

    OnGround	  = 0x1000   # weight-on-wheels
    FlcsBitRun    = 0x2000   # FLT CONTROL panel RUN light (used to be Multi-engine fire light)
    FlcsBitFail   = 0x4000   # FLT CONTROL panel FAIL light (used to be Lock light Cue; non-F-16)
    DbuWarn       = 0x8000   # Right eyebrow DBU ON cell; was Shoot light cue; non-F16
    NoseGearDown  = 0x10000  # Landing gear panel; on means down and locked
    LeftGearDown  = 0x20000  # Landing gear panel; on means down and locked
    RightGearDown = 0x40000  # Landing gear panel; on means down and locked
    ParkBrakeOn   = 0x100000 # Parking brake engaged; NOTE: not a lamp bit
    Power_Off     = 0x200000 # Set if there is no electrical power.  NB: not a lamp bit

    # Caution panel
    cadc	= 0x400000

    # Left Aux console
    SpeedBrake = 0x800000  # True if speed brake is in anything other than stowed position

    # Threat Warning Prime - additional bits
    SysTest  = 0x1000000

    # Master Caution WILL come up (actual lightBit has 3sec delay like in RL)
    # usable for cockpit builders with RL equipment which has a delay on its own.
    # Will be set to false again as soon as the MasterCaution bit is set.
    MCAnnounced = 0x2000000

    #MLGWOW is only for AFM  it means WOW switches on MLG are triggered => FLCS switches to WOWPitchRockGain
    MLGWOW = 0x4000000
    NLGWOW = 0x8000000

    ATF_Not_Engaged = 0x10000000

    # Free bits in LightBits3
    #0x20000000
    #0x40000000
    #0x80000000

    # Used with the MAL/IND light code to light up "everything"
    # please update this if you add/change bits!
    AllLampBits3On = 0x1147EFFF
    AllLampBits3OnExceptCarapace = AllLampBits3On ^ SysTest

class HsiBits(Enum):
    ToTrue        = 0x01    # HSI_FLAG_TO_TRUE == 1 TO
    IlsWarning    = 0x02    # HSI_FLAG_ILS_WARN
    CourseWarning = 0x04    # HSI_FLAG_CRS_WARN
    Init          = 0x08    # HSI_FLAG_INIT
    TotalFlags    = 0x10    # HSI_FLAG_TOTAL_FLAGS; never set
    ADI_OFF       = 0x20    # ADI OFF Flag
    ADI_AUX       = 0x40    # ADI AUX Flag
    ADI_GS        = 0x80    # ADI GS FLAG
    ADI_LOC       = 0x100   # ADI LOC FLAG
    HSI_OFF       = 0x200   # HSI OFF Flag
    BUP_ADI_OFF   = 0x400   # Backup ADI Off Flag
    VVI           = 0x800   # VVI OFF Flag
    AOA           = 0x1000  # AOA OFF Flag
    AVTR          = 0x2000  # AVTR Light
    OuterMarker   = 0x4000  # MARKER beacon light for outer marker
    MiddleMarker  = 0x8000  # MARKER beacon light for middle marker
    FromTrue      = 0x10000 # HSI_FLAG_TO_TRUE == 2 FROM

    Flying		  = 0x80000000 # true if player is attached to an aircraft (i.e. not in UI state).  NOTE: Not a lamp bit

    # Used with the MAL/IND light code to light up "everything"
    # please update this is you add/change bits!
    AllLampHsiBitsOn = 0xE000

###########################################################################################################

def parsejson_lightBits():
    # global lock,datalist
    BmsInterface.srvlock.acquire()
    if len(BmsInterface.datalist)>0:
        try:
            obj = json.loads(BmsInterface.datalist[0])
            BmsInterface.srvlock.release()
            if obj is not None:
                lenth=len(obj)
                if lenth>1:
                    return obj["lightBits"],obj["lightBits2"],obj["lightBits3"]
        except ZeroDivisionError,e:
            BmsInterface.srvlock.release()
    BmsInterface.srvlock.release()

    return 0,0,0


def is_dead():
    try:
        lb1, lb2, lb3 = parsejson_lightBits()
        if (lb1 & LightBits1.MasterCaution)>0 \
                or (lb1 & LightBits1.ENG_FIRE)>0 \
                or (lb1 & LightBits1.FLCS) >0\
                or (lb2 & LightBits2.ENGINE) >0\
                or (lb3 & LightBits3.Elec_Fault) >0:
            logger.warn("dead ... %s, %s, %s" % (lb1, lb2, lb3))
            return True
        else:
            logger.debug("alive ... %s, %s, %s" % (lb1, lb2, lb3))
            return False

    except (IOError,ZeroDivisionError,NameError,TypeError,SyntaxError,ValueError),e:
        logger.error("exception: %s" % (e))