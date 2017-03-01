
alarm = None
comms = None

DING1 = 'sounds/coin1.wav'
DING2 = 'sounds/coin2.wav'


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
