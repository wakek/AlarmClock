from kivy import require as kivy_require
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.app import App
from time import asctime
from datetime import datetime
import Logger


class ClockText(Label):
    def __init__(self, **kwargs):
        super(ClockText, self).__init__(**kwargs)
        update_clock(self)

    def update(self, *args):
        self.text = asctime()


def update_clock(clock):
    Clock.schedule_interval(clock.update, 1)


# ----------------------------------------------- Window Manager -----------------------------------------------
class WindowManager(ScreenManager):
    pass
# ----------------------------------------------- Window Manager -----------------------------------------------


# -------------------------------------------- Screens: Main Screen --------------------------------------------
class MainWindow(Screen):
    def add_alarm(self, alarm_entry, alarm_repeat, days, list_view):
        if 'Hour' in alarm_entry or 'Minute' in alarm_entry:
            return
        Logger.log_info_message('Adding new alarm: ' + alarm_entry)
        repeat_days = []
        if alarm_repeat == 'down':
            for day in days.children[::-1]:
                if day.state == 'down':
                    repeat_days.append(day.text)
        alarm_entry = '{0}, Repeat On: {1}'.format(alarm_entry, ','.join(repeat_days))
        new_alarm = Label(text=alarm_entry, size_hint=(1, None))
        new_alarm.height = new_alarm.texture_size[1]
        new_alarm.text_size = (300, None)
        list_view.add_widget(new_alarm)
        Clock.schedule_interval(lambda x: sound_alarms(list_view), 1)


def sound_alarms(list_view):
    for child in list_view.children[::-1]:
        if child.text == '' or child.text == 'Welcome':
            continue
        now = datetime.now()
        alarm_time_details = child.text.split(', Repeat On:')
        weekdays = {'Su': 1, 'Mo': 2, 'Tu': 3, 'We': 4, 'Th': 5, 'Fr': 6, 'Sa': 7}
        alarm_time = now.replace(hour=int(alarm_time_details[0].split(':')[0]), minute=int(alarm_time_details[0].split(':')[1]))
        Logger.log_info_message('Comparing datetimes {} and {}'.format(now, alarm_time))
        if alarm_time_details[1] != ' ':
            alarm_repeat_days = alarm_time_details[1].split(',')
            for repeat_day in alarm_repeat_days:
                if now.weekday() != weekdays[repeat_day] or now != alarm_time:
                    return

        sound = SoundLoader.load('looperman-the-story-behind-a-smile-1.wav')
        if sound and now == alarm_time:
            Logger.log_info_message("Sound found at {}".format(sound.source))
            Logger.log_info_message("Sound is {} seconds".format(sound.length))
            sound.play()
            if alarm_time_details[1] == ' ':
                list_view.remove_widget(child)


# -------------------------------------------- Screens: Main Screen --------------------------------------------


class MainApp(App):

    kivy_require('1.0.1')
    # kv = Builder.load_file(r'main.kv')

    def build(self):
        Logger.log_info_message('Building main app')
        sm = WindowManager()
        return sm