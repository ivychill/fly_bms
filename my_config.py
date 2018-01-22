# my_config.py
import logging.handlers
import os

#global logger
# def init():
#     global logger
def check_log_dir(dir_name):
    #dir = os.path.dirname(dir_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    else:
        pass
    #is_training = True         #True means Train, False means simply Run
    #max_eps = 1000000
    #test_eps = 10

LOG_PATH = './log'
MAX_LOG_SIZE = 2560000
LOG_BACKUP_NUM = 4000
# creat logger
check_log_dir(LOG_PATH)
logger = logging.getLogger('AirCombat')
log_file = os.path.join(LOG_PATH, 'control.log')
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=MAX_LOG_SIZE, backupCount=LOG_BACKUP_NUM)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
# logger.addHandler(consoleHandler)
logger.setLevel(logging.DEBUG)