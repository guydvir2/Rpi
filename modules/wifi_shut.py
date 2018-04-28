import cbit
import subprocess
import getip
from sys import platform
import datetime


class Time2Start:
    def __init__(self):
        self.cbit = cbit.CBit(500)
        self.clock_format = '%H:%M:%S'
        self.date_format = '%Y-%m-%d'
        task1 = {'start_days': [4, 3], 'start_time': '21:30:00', 'end_days': [5, 3], 'end_time': '22:00:00'}
        self.cbit.append_process(self.weekly_time_to_task, wtask=task1)
        self.cbit.init_thread()

    def create_date_from_string(self, date, clock):
        c = datetime.datetime.strptime(clock, self.clock_format)
        d = datetime.datetime.strptime(date, self.date_format)
        full_date = datetime.datetime.combine(d.date(), c.time())
        return full_date

    def time_now(self):
        return datetime.datetime.now()

    def calc_remain_time(self, t1, t2):
        return (t1 - t2)

    def weekly_time_to_task(self, wtask):
        # for loop for multiple days in task
        for i, day_task_start in enumerate(wtask['start_days']):
            day_task_end = wtask['end_days'][i]
            timenow = self.time_now()
            delta_time_start = datetime.datetime.combine(timenow.date(),
                                                         datetime.datetime.strptime(wtask['start_time'],
                                                                                    self.clock_format).time()) - timenow
            delta_time_end = datetime.datetime.combine(timenow.date(),
                                                       datetime.datetime.strptime(wtask['end_time'],
                                                                                  self.clock_format).time()) - datetime.datetime.combine(
                timenow.date(),
                datetime.datetime.strptime(wtask['start_time'], self.clock_format).time())

            delta_days_start = day_task_start - timenow.isoweekday()
            if delta_days_start < 0:
                delta_days_start += 7
            time_to_start = datetime.timedelta(days=delta_days_start) + delta_time_start

            delta_days_end = day_task_end - day_task_start
            if delta_days_end < 0:
                delta_days_end += 7
            time_to_end = datetime.timedelta(days=delta_days_end) + delta_time_end + time_to_start

            print(time_to_start, time_to_end)


class WifiControl:
    def __init__(self):
        self.plat = platform
        print('booted on %s system' % self.plat)
        self.wifi_command = 'nmcli radio wifi'.split()
        self.pwd = None

    def wifi_change_state(self, state):
        if state.upper() in ['ON', 'OFF']:
            updated_command = self.wifi_command + [state.lower()]
            a1 = subprocess.Popen(['sudo', '-S'] + updated_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                  universal_newlines=True)
            a1.communicate(self.pwd + '\n')[1]

    def read_pwd_fromfile(self):
        filename = '/home/guy/Documents/github/Rpi/modules/p.txt'
        with open(filename, 'r')as f:
            self.pwd = f.read()

    def get_status(self):
        a1 = subprocess.Popen(['nmcli', 'radio', 'all'], stdout=subprocess.PIPE)
        tup_output = a1.communicate()
        print(tup_output)

    def wifi_off(self):
        self.wifi_change_state('off')
        self.get_status()

    def wifi_on(self):
        try:
            self.wifi_change_state('on')
            self.get_status()
        except OSError:
            print('NO NETWORK')
        print(self.verify_ip())

    def verify_ip(self):
        print(getip.get_ip())


# a = WifiControl()
# a.read_pwd_fromfile()
# a.wifi_on()

b = Time2Start()
