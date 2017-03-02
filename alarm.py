import threading
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


class Profile:
    def __init__(self, alarm=False, running=False, no_weekends=True):
        self.alarm_on = alarm
        self.running = running
        self.no_weekends = no_weekends
        self.snoozing = False
        self.alarm = datetime.datetime.now()


class Alarm(threading.Thread):
    def __init__(self, comms):
        threading.Thread.__init__(self)
        self.comms_system = comms

        self.profiles = [Profile(), Profile()]
        self.load_profiles()

        self.scheduler = BackgroundScheduler(timezone="EST")
        self.scheduler.start()
        self.comms_system.log('alarm init complete')

        # TODO: in case we're recovering from a crash, check if alarms need to be scheduled
        for profile in self.profiles:
            if profile.alarm_on:
                alarm = profile.alarm
                task_id = str(self.profiles.index(profile))
                try:
                    self.scheduler.add_job(lambda: self.sound_alarm(profile), 'date', run_date=alarm,
                                           id=task_id, replace_existing=True)
                except Exception as ee:
                    print("Error recovering alarms: " + ee.__str__())
                    self.comms_system.log("Error recovering alarms: " + ee.__str__())

    def now(self):
        now = datetime.datetime.now()
        return now.strftime("%I:%M:%S %p")

    def fetch(self, profile_index):
        alarm = self.profiles[profile_index].alarm.strftime("%I:%M:%S %p\n")
        alarm_day = self.profiles[profile_index].alarm.strftime("%b %d, %Y\n")
        if self.profiles[profile_index].alarm_on:
            alarm_on = "alarm enabled\n"
        else:
            alarm_on = "alarm disabled\n"
        if self.profiles[profile_index].no_weekends:
            weekends = "skip weekends\n"
        else:
            weekends = "include weekends\n"
        return alarm + alarm_day + alarm_on + weekends

    def save_profiles(self):
        self.comms_system.save_obj(self.profiles, 'profile')

    def load_profiles(self):
        p = self.comms_system.load_obj('profile')
        if p:
            self.profiles = p
        else:
            self.comms_system.save_obj(self.profiles, 'profile')

    def set_next_alarm(self, p):
        # add a day to the alarm
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        p.alarm = p.alarm.replace(day=tomorrow.day, month=tomorrow.month, year=tomorrow.year)
        p.alarm = datetime.datetime.now() + datetime.timedelta(seconds=5)
        alarm = p.alarm

        while p.alarm.weekday() > 4 and p.no_weekends:
            p.alarm += datetime.timedelta(days=1)
        try:
            print(self.scheduler.get_jobs())
            self.scheduler.add_job(lambda: self.sound_alarm(p), 'date', run_date=alarm,
                                   id=task_id, replace_existing=True)
        except Exception as ee:
            print("Error adding: " + ee.__str__())
        self.save_profiles()

    def sound_alarm(self, profile):
        profile.running = True
        task_id = str(self.profiles.index(profile))
        self.comms_system.log('Waking up ' + task_id)
        self.comms_system.aio_send(task_id, "waking")
        self.comms_system.ifttt('wakeup', task_id)
        self.comms_system.play_speech("Good morning. It is time for you to wake up.")

    def snooze(self, profile):
        task_id = str(self.profiles.index(profile))
        self.comms_system.log('Snoozing ' + task_id)
        self.comms_system.aio_send(task_id, 'snoozing')
        self.comms_system.ifttt('snoozing', task_id)

    def stop_alarm(self):
        for profile in self.profiles:
            if profile.running:
                task_id = str(self.profiles.index(profile))
                profile.running = False
                if profile.alarm_on:
                    self.set_next_alarm(profile)
                self.comms_system.log('Alarm stopped ' + task_id)
                self.comms_system.aio_send(task_id, 'awake')
                self.comms_system.ifttt('awake', task_id)

    def adjust_alarm(self, profile, change):
        if profile.endswith('1'):
            p = self.profiles[0]
        else:
            p = self.profiles[1]
        if "hour" in change:
            if change.endswith('+'):
                p.alarm += datetime.timedelta(hours=1)
            else:
                p.alarm -= datetime.timedelta(hours=1)
        elif "min" in change:
            if change.endswith('+'):
                p.alarm += datetime.timedelta(minutes=1)
            else:
                p.alarm -= datetime.timedelta(minutes=1)
        elif 'toggle' in change:
            p.alarm_on = not p.alarm_on
            if p.alarm_on:
                self.set_next_alarm(p)
            else:
                try:
                    task_id = str(self.profiles.index(p))
                    self.scheduler.remove_job(task_id)
                except Exception as ee:
                    print("Error in removal: " + ee.__str__())
        elif 'weekend' in change:
            p.no_weekends = not p.no_weekends
        self.save_profiles()
