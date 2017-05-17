import helper
import kivy
import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.clock import Clock

kivy.require("1.9.1")
Config.set('graphics', 'fullscreen', '1')

os.environ['DISPLAY'] = ":0"


class HomeScreen(Screen):
    pass


class AlarmScreen(Screen):
    pass


class LightScreen(Screen):
    pass


class MediaScreen(Screen):
    pass


class OptionScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


class TriggerScreen(Screen):
    pass


class Profile1(Label):
    def __init__(self, **kwargs):
        # kivy stuff
        super(Profile1, self).__init__(**kwargs)


class Profile2(Label):
    def __init__(self, **kwargs):
        # kivy stuff
        super(Profile2, self).__init__(**kwargs)


class LightLabel(Label):
    def __init__(self, **kwargs):
        # kivy stuff
        super(LightLabel, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        comms = helper.get_comms()
        ## DISPLAY DETECTED USERS HERE
        self.text = "Hello Light Label!"
        answer = comms.check_bluetooth('08:ec:a9:0f:88:3e')
        self.text = self.text + str(answer)
        
class SystemInfo(Label):
    def __init__(self, **kwargs):
        # kivy stuff
        super(SystemInfo, self).__init__(**kwargs)


class StatusBox(BoxLayout):
    def __init__(self, **kwargs):
        # kivy stuff
        super(StatusBox, self).__init__(**kwargs)
        # make the button update
        Clock.schedule_interval(self.update, .1)
        self.id = 'status'
        self.alarm = helper.get_alarm()
        self.p1 = Profile1()
        self.p2 = Profile2()
        self.sys = SystemInfo()
        self.add_widget(self.p1)
        self.add_widget(self.sys)
        self.add_widget(self.p2)

    def update(self, *args):
        self.p1.text = self.alarm.fetch(0)
        self.p2.text = self.alarm.fetch(1)
        self.sys.text = self.alarm.now()
        for profile in self.alarm.profiles:
            if profile.running:
                # if the alarm is running, change screen
                App.get_running_app().root.current = 'trigger'
                comms = helper.get_comms()
                comms.play_fx(helper.DING2)


class MyButton(Button):
    def __init__(self, **kwargs):
        # kivy stuff
        super(MyButton, self).__init__(**kwargs)
        self.alarm = helper.get_alarm()
        self.active_profile = "PROFILE 1"

    def ding1(self):
        helper.comms.play_fx(helper.DING1)

    def ding2(self):
        helper.comms.play_fx(helper.DING2)

    def adjust_alarm(self, btn, change):
        self.alarm.adjust_alarm(btn.text, change)


class MyProfileButton(MyButton):
    def __init__(self, **kwargs):
        # kivy stuff
        super(MyProfileButton, self).__init__(**kwargs)
        self.active_profile = "PROFILE 1"

    def switch_profile(self):
        if self.active_profile == "PROFILE 2":

            self.active_profile = "PROFILE 1"
        else:
            self.active_profile = "PROFILE 2"
        self.text = self.active_profile
