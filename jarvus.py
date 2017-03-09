import gui  # needed for kivy objects
import comms
import alarm
import helper
import subprocess
import rpi_backlight as bl

from kivy.app import App
from kivy.lang import Builder


class Jarvus(App):
    comms_system = comms.Comms()
    alarm = alarm.Alarm(comms_system)
    screen_on = True
    backlight = bl

    def build(self):
        # comms thread
        self.comms_system.setDaemon(True)
        self.comms_system.start()
        self.comms_system.log('comms started')
        # alarm thread
        self.alarm.setDaemon(True)
        self.alarm.start()
        self.comms_system.log('alarm started')
        # pass threads to a helper to make more accessible
        helper.set_alarm(self.alarm)
        helper.set_comms(self.comms_system)

        self.backlight = bl
        self.backlight.set_power(True)
        self.screen_on = True

        this_app = Builder.load_file('gui.kv')
        return this_app

    def screen_toggle(self):
        print('Turning screen off')
        # Doesn't work
        try:
            if self.screen_on():
                self.backlight.set_power(False)
                self.screen_on = False
                self.comms_system.play_fx(helper.DING1)

            else:
                self.backlight.set_power(True)
                self.screen_on = True
                self.comms_system.play_fx(helper.DING2)

        except Exception as ee:
            self.comms_system.log("Back light toggle failed: " + ee.__str__())
            return

    # bouncing command from kivy to alarm thread
    def stop_alarm(self):
        self.alarm.stop_alarm()


try:
    if __name__ == '__main__':
        Jarvus().run()
        helper.comms.log("Jarvus no longer running.")
        pass

except (KeyboardInterrupt, SystemExit):
    helper.comms.log("Jarvus logging out. Goodbye.")
    pass

except Exception as e:
    helper.comms.log("Jarvus failed: " + e.__str__())
    pass
