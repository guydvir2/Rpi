import cbit
import subprocess
import getip
from sys import platform
import datetime


class Time2Start:
    def __init__(self):
        self.tasks_status, self.tasks = [], []
        self.clock_format = '%H:%M:%S'
        self.date_format = '%Y-%m-%d'
        self.cbit = cbit.CBit(500)
        # self.cbit.append_process(self.weekly_tasks_schedule, wtask=task1)
        self.cbit.init_thread()

    def weekly_tasks_schedule(self, wtask):
        # for loop for multiple days in task
        self.tasks_status.append([])
        for i, day_task_start in enumerate(wtask['start_days']):
            status_dict = {}
            self.tasks_status[-1].append([])
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

            status_dict['start'] = time_to_start
            status_dict["end"] = time_to_end
            if time_to_start.total_seconds() < 0:
                if time_to_end.total_seconds() > 0:
                    status_dict['state'] = 1
            else:
                status_dict['state'] = 0
            self.tasks_status[-1][i] = status_dict
        return self.tasks_status

    def time_now(self):
        return datetime.datetime.now()

    def add_task(self, new_task):
        self.tasks.append(new_task)

    def run_tasks(self):
        b = list(map(self.weekly_tasks_schedule, self.tasks))[0]
        # pr = lambda status: status
        # print(list(map(pr, b[0][0])))
        print(b[1][0]['start'])
        # print(b[0][0])  # [1][0]['start'])
        # for i, task in enumerate(self.tasks):
        #     self.weekly_tasks_schedule(wtask=task)

    # def create_date_from_string(self, date, clock):
    #     c = datetime.datetime.strptime(clock, self.clock_format)
    #     d = datetime.datetime.strptime(date, self.date_format)
    #     full_date = datetime.datetime.combine(d.date(), c.time())
    #     return full_date

    # def calc_remain_time(self, t1, t2):
    #     return (t1 - t2)


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
b.add_task(new_task={'start_days': [4, 3], 'start_time': '21:30:00', 'end_days': [5, 3], 'end_time': '22:00:00'})
b.add_task(new_task={'start_days': [7], 'start_time': '07:30:00', 'end_days': [7], 'end_time': '22:35:00'})
#
b.run_tasks()
