import threading
import logging
import pygame
import subprocess
import requests
import pickle
import Private
import os
from Adafruit_IO import Client, Feed


class Comms(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        # LOGGING
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        # create a file handler
        log_handler = logging.FileHandler('log_jarvus.log')
        log_handler.setLevel(logging.INFO)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_handler.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(log_handler)
        self.log('comms init complete')
        self.phue_status = self.connect_phue()
        self.p1_status = "home"
        self.p2_status = "home"
        pygame.mixer.init()
        self.aio = Client(Private.Private.AIO_KEY)
        # bluetooth in try-block to allow clients to run without pybluez module
        try:
            # noinspection PyUnresolvedReferences
            import bluetooth
        except ImportError:
            self.log("Failed to import bluetooth")
            pass

    def log(self, msg):
        self.logger.info(msg)

    # PICKLE
    def save_obj(self, obj, name):
        self.log("Saving " + name)
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + '/obj/' + name + '.pkl', 'wb') as f:
                pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        except Exception as ee:
            self.log("Error saving object " + name + ee.__str__())

    def load_obj(self, name):
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + '/obj/' + name + '.pkl', 'rb') as f:
                return pickle.load(f)
        except Exception as ee:
            self.log("Error loading object " + name + ee.__str__())
            return None

    # BLUETOOTH
    def check_bluetooth(self, target):
        # check to see if Laura is home
        try:
            result = bluetooth.lookup_name(target, timeout=5)
            if result is not None:
                return True
            else:
                return False

        except Exception as ee:
            self.log("Failed bluetooth lookup" + ee.__str__())
            return False

    def connect_phue(self):
        try:
            from phue import Bridge
        except Exception as ee:
            self.log("Error loading phue: " + ee.__str__())
            return False

        try:
            b = Bridge(Private.Private.BRIDGE_IP)
            b.connect()
        except Exception as ee:
            self.log("Error connecting phue: " + ee.__str__())
            return False
        self.log("phue connected")
        return True

    # ADAFRUIT.IO
    def aio_send(self, feed, msg):
        try:
            self.aio.send(feed, msg)
        except Exception as ee:
            self.log("Failed to send to AIO: " + msg + ee.__str__())
            return

    def aio_create_feed(self, feed):
        try:
            self.aio.create_feed(feed)
        except Exception as ee:
            self.log("Failed to create feed: " + ee.__str__())
            return

    #  IFTTT
    def ifttt(self, val1='hello', val2='hello', val3='hello'):
        try:
            payload = "{ 'value1' : %s, 'value2' : %s, 'value3' : %s}" % (val1, val2, val3)
            requests.post("https://maker.ifttt.com/trigger/wakeup/with/key/" + Private.Private.MAKER_SECRET, data=payload)
        except Exception as ee:
            self.log("Failed to post to IFTTT: " + ee.__str__())
            return

    #  AUDIO
    def play_fx(self, file, loop=0):
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(loop)
        except Exception as ee:
            self.log("Play sound fx failed: " + ee.__str__())
            return

    def play_speech(self, text):
        try:
            bash_command = "echo '" + text + "' | festival --tts"
            subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        except Exception as ee:
            self.log("Playing festival tts failed: " + ee.__str__())
            return

