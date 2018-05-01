import cbit
import subprocess
import getip
from sys import platform
import datetime


class Time2Start:
    def __init__(self):
        self.tasks_status, self.weekly_tasks_list = [], []
        self.clock_format = '%H:%M:%S'
        self.date_format = '%Y-%m-%d'
        self.cbit = cbit.CBit(500)

    def swipe_weekly_schedule(self, wtask):
        task_output_result = []
        # for loop for multiple days in task
        for i, day_task_start in enumerate(wtask['start_days']):
            status_dict = {}
            # self.tasks_status[-1].append([])
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
            task_output_result.append(status_dict)

        return task_output_result

    def exec_tasks_run(self):
        self.tasks_status = [[] for i in range(len(self.weekly_tasks_list))]

        def is_any_task_on():
            result = []
            for m, task in enumerate(self.tasks_status):
                for n, sub_task in enumerate(task):
                    if sub_task['state'] == 1:
                        result.append([m, n])
            if result == []:
                result.append(0)
            return result

        def inject_tasks_to_schedule():
            self.tasks_status = list(map(self.swipe_weekly_schedule, self.weekly_tasks_list))
            print(is_any_task_on())
            # print_task_status = lambda status, i=0: print(
            #     'Task:%d, Start:%s, Stop:%s, Status:%s, duration:%s' % (i, str(status[i]['start'])[:-7],
            #                                                             str(status[i]['end'])[:-7],
            #                                                             status[i]['state'],
            #                                                             (status[i]['end'] - status[i]['start'])))
            # list(map(print_task_status, self.tasks_status))

            # print(self.tasks_status)
            # for i, task in enumerate(self.weekly_tasks_list):
            #     self.tasks_status[i] = self.swipe_weekly_schedule(task)

        self.cbit.append_process(inject_tasks_to_schedule)
        self.cbit.init_thread()

    def time_now(self):
        return datetime.datetime.now()

    def add_weekly_task(self, new_task):
        self.weekly_tasks_list.append(new_task)

    # def create_date_from_string(self, date, clock):
    #     c = datetime.datetime.strptime(clock, self.clock_format)
    #     d = datetime.datetime.strptime(date, self.date_format)
    #     full_date = datetime.datetime.combine(d.date(), c.time())
    #     return full_date


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
b.add_weekly_task(new_task={'start_days': [1, 3], 'start_time': '11:30:00', 'end_days': [5, 3], 'end_time': '22:00:00'})
b.add_weekly_task(new_task={'start_days': [7], 'start_time': '07:30:00', 'end_days': [7], 'end_time': '22:35:00'})
#
b.exec_tasks_run()
