import os
from inspect import getsourcefile
from os.path import abspath

alarm = None
comms = None

whole_path = abspath(getsourcefile(lambda: 0))
sep = "JarvusPi/"
path = whole_path.split(sep, 1)[0]
DING1 = path + 'JarvusPi/sounds/coin1.wav'
DING2 = path + 'JarvusPi/sounds/coin2.wav'


def set_alarm(alarm_thread):
    global alarm
    alarm = alarm_thread


def set_comms(comms_thread):
    global comms
    comms = comms_thread


def get_comms():
    global comms
    return comms


def get_alarm():
    global alarm
    return alarm
