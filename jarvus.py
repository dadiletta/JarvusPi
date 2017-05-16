import gui  # needed for kivy objects even if it says it's not used
import os
import logging
import comms
import alarm
import helper
import webbrowser
import subprocess
import rpi_backlight as bl

from kivy.app import App
from kivy.lang import Builder


class Jarvus(App):
    # declared as static class variables (rather than in an __init__ method) --- NOT IDEAL
    comms_system = comms.Comms()        # communication thread
    alarm = alarm.Alarm(comms_system)   # alarm thread
    screen_on = True    # old method to keep track of screen power
    backlight = bl      # new control of screen power

    def build(self):
        # comms thread
        self.comms_system.setDaemon(True)
        self.comms_system.start()
        self.comms_system.logger.info('comms has started')
        # alarm thread
        self.alarm.setDaemon(True)
        self.alarm.start()
        self.comms_system.logger.debug('alarm thread started')
        # pass threads to a helper to make more accessible
        helper.set_alarm(self.alarm)
        helper.set_comms(self.comms_system)

        try:
            self.backlight = bl
            self.backlight.set_power(True)
            self.screen_on = True
        except Exception as ee:
            self.comms_system.logger.error('Backlight failed: ' + ee.__str__())

        this_app = Builder.load_file('gui.kv')
        return this_app

    def load_youtube(self):
        self.comms_system.logger.debug("load_youtube called")
        webbrowser.open("http://youtube.com/", new=1, autoraise=True)
        try:
            bash_command = "x-www-browser http://youtube.com"
            subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        except Exception as ee:
            self.comms_system.logger.error("Web browser command failed: " + ee.__str__())
            return

    def backlight_on(self):
        self.comms_system.logger.debug("backlight_on called")
        try:
            self.backlight.set_power(True)
        except Exception as ee:
            self.comms_system.logger.error('Failed backlight: ' + ee.__str__())

    def screen_toggle(self):
        self.comms_system.logger.debug('Turning screen off')
        # Doesn't work
        if self.screen_on:
            self.backlight.set_power(False)
            self.screen_on = False
            self.comms_system.play_fx(helper.DING1)

        else:
            self.backlight.set_power(True)
            self.screen_on = True
            self.comms_system.play_fx(helper.DING2)


    # bouncing command from kivy to alarm thread
    def stop_alarm(self):
        self.alarm.stop_alarm()

try:
    if __name__ == '__main__':
        Jarvus().run()
        logging.info("Jarvus no longer running.")
        pass

except (KeyboardInterrupt, SystemExit):
    logging.info("Jarvus logging out by interrupt. Goodbye.")
    pass

except Exception as e:
    logging.error("Jarvus failed: " + e.__str__())
    pass
