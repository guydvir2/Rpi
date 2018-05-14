import cbit
import subprocess
import getip
from sys import platform
import datetime
import os
import csv


class WeeklyIntervals:
    """Class creates a datetime tuples for a recurring weekly tasks.
    Inputs: start day and time, end date and time
    Outputs: start and end datetime tuples for current week"""

    def __init__(self, day_start, hour_start, day_end, hour_end):
        self.day_start = day_start
        self.day_end = day_end
        self.hour_start = hour_start
        self.hour_end = hour_end

    def day_shift_time_tuple(self, delta_days, time):
        """create a datetime tuple of shifted day- days and clock"""
        clock_format = '%H:%M:%S'
        clock = datetime.datetime.strptime(time, clock_format)

        shifted_datetime = datetime.datetime.combine(
            datetime.datetime.now().date() + datetime.timedelta(days=delta_days), clock.time())
        return shifted_datetime

    def shift_from_toady_time_tuple(self, day, hour):
        shifted_datetime = self.day_shift_time_tuple(day - self.iso2h_day_convert(datetime.datetime.now().isoweekday()),
                                                     hour)
        return shifted_datetime

    def iso2h_day_convert(self, iso_day):
        if 1 <= iso_day <= 6:
            day = iso_day + 1
        elif iso_day == 7:
            day = 1
        else:
            day = None
        return day

    def h2iso_convert_day(self, day):
        if 2 <= day <= 7:
            iso_day = day - 1
        elif day == 1:
            iso_day = 7
        return iso_day

    def get_datetimes(self):
        start_datetime = self.shift_from_toady_time_tuple(self.day_start, self.hour_start)
        if self.day_end - self.day_start >= 0:
            end_datetime = self.shift_from_toady_time_tuple(self.day_end, self.hour_end)
        else:
            end_datetime = self.shift_from_toady_time_tuple(self.day_end + 7, self.hour_end)

        # if start_datetime > end_datetime:
        #     end_datetime += datetime.timedelta(days=7)
        return start_datetime, end_datetime


class RunWeeklySchedule:
    """Class gets a weekly schedule (day and time on/ off ) and in return it submits
    a status: which task is on/off and when it starts/ ends.
    inputs: lists of schedule -
    new_task={'start_days': [1, 4], 'start_time': '15:30:00', 'end_days': [5, 6], 'end_time': '22:00:00'}
    outputs: variations of on/ off status"""

    def __init__(self, on_func, off_func, sched_file=None, ext_cond=None):
        self.tasks_status, self.previous_task_status, self.weekly_tasks_list = [], [], []
        self.engage_task, self.tasks_dates, self.on_tasks = [], [], []
        self.on_func, self.off_func, self.ext_cond = on_func, off_func, ext_cond
        self.filename = sched_file
        self.cbit = cbit.CBit(500)
        """Engage flag gives the ability to enable or disable on/off regardless"""

    def add_weekly_task(self, new_task):
        self.weekly_tasks_list.append(new_task)
        # method indicates if start an active schedule
        days = len(new_task['start_days'])
        self.engage_task.append([1] * days)
        self.previous_task_status.append([{'state': 0}] * days)

    def read_sched_file(self, file_in=''):
        if file_in == '':
            file_in = self.filename
        if os.path.isfile(file_in) is True:
            with open(file_in, 'r') as f:
                reader = csv.reader(f)
                self.data_from_file = list(reader)
        else:
            print('Schedule file was not found on specified location', file_in)

    def validate_schedule(self):
        # Check if schedule inputs and valid
        time_format = "%H:%M:%S"

        for i, task in enumerate(self.weekly_tasks_list):
            try:
                datetime.datetime.strptime(task['start_time'], time_format)
                datetime.datetime.strptime(task['end_time'], time_format)
            except ValueError:
                print('bad time format: ', task)
                del self.weekly_tasks_list[i]
                break

            cond1 = all(list(map(lambda x: 0 < int(x) < 8, task['start_days'])))
            cond2 = all(list(map(lambda x: 0 < int(x) < 8, task['end_days'])))
            if not cond1 or not cond2:
                print('bad day format: ', task)
                del self.weekly_tasks_list[i]
                break

    def convert_data_file(self):
        dict = []
        a1 = lambda a: a.split(',')
        for i, task in enumerate(self.data_from_file):
            dict.append({})
            dict[i]['start_days'] = list(map(lambda x: int(x), a1(task[0])))
            dict[i]['start_time'] = task[1]
            dict[i]['end_days'] = list(map(lambda x: int(x), a1(task[2])))
            dict[i]['end_time'] = task[3]
        return dict

    def start(self):
        # Case of reading schedule from file
        if not self.weekly_tasks_list and self.filename is not None:
            self.read_sched_file()
            print('Schedule file read successfully')
            for task in self.convert_data_file():
                self.add_weekly_task(task)
        # Case of getting schedule in code
        elif self.weekly_tasks_list:
            print('Schedule read as code arguments')
        # Neither
        else:
            print('Schedule not read properly. Abort!')
            quit()

        self.validate_schedule()
        self.convert_weekly_tasks_to_dates()
        self.run_schedule()
        self.tasks_descriptive()

    def convert_weekly_tasks_to_dates(self):
        self.tasks_dates = []
        for n, task in enumerate(self.weekly_tasks_list):
            self.tasks_dates.append([])
            for i, day_task_start in enumerate(task['start_days']):
                self.tasks_dates[-1].append([])
                status_dict = {}
                day_task_end = task['end_days'][i]
                status_dict['start'], status_dict['end'] = WeeklyIntervals(day_start=day_task_start,
                                                                           hour_start=task['start_time'],
                                                                           day_end=day_task_end,
                                                                           hour_end=task['end_time']).get_datetimes()
                self.tasks_dates[n][i] = status_dict

    def update_tasks_times(self):
        # Decide if "ON" or "OFF" state
        self.tasks_status = []
        for m, task in enumerate(self.tasks_dates):
            self.tasks_status.append([])
            for n, current_day in enumerate(task):
                self.tasks_status[m].append([])
                self.tasks_status[m][n] = current_day.copy()
                if current_day['start'] <= datetime.datetime.now() <= current_day['end']:
                    self.tasks_status[m][n]['state'] = 1
                else:
                    self.tasks_status[m][n]['state'] = 0

    def run_schedule(self):  # constant run on cbit

        def act_on_change(changed_task):
            if self.tasks_status[changed_task[0]][changed_task[1]]['state'] == 1:
                self.on_func()
            elif self.tasks_status[changed_task[0]][changed_task[1]]['state'] == 0:
                self.off_func()
                self.convert_weekly_tasks_to_dates()
            self.get_task_report(changed_task)

        def check_conditions_to_switch():
            result = []
            for m, task in enumerate(self.tasks_status):
                for n, sub_task in enumerate(task):
                    if sub_task['state'] == 1 and self.engage_task[m][n] == 1:
                        result.append([m, n])
                    if sub_task['state'] != self.previous_task_status[m][n]['state']:
                        act_on_change([m, n])
                    # case of external condition to be verified
                    if sub_task['state'] == self.engage_task[m][n] and self.engage_task[m][
                        n] != self.ext_cond and self.ext_cond != None:
                        act_on_change([m, n])
            self.on_tasks = result
            self.previous_task_status = self.tasks_status.copy()

        def inject_tasks_to_schedule():
            """ update tasks using cbit """
            self.update_tasks_times()
            check_conditions_to_switch()

        self.cbit.append_process(inject_tasks_to_schedule)
        self.cbit.init_thread()

    def tasks_descriptive(self):
        for m, task in enumerate(self.tasks_dates):
            for n, day in enumerate(task):
                t = [datetime.datetime.strftime(day['start'], 'Start-[%A, %H:%M:%S]'),
                     datetime.datetime.strftime(day['end'], 'End- [%A, %H:%M:%S]')]
                print('Task #%d/#%d: %s %s' % (m, n, t[0], t[1]))

    def get_task_report(self, task=None):
        now = datetime.datetime.now()

        def print_report(state):
            print('Task #%d/%d:[%s:%s], start:[%s], end:[%s]' % (
                i, m, state, str(now - sub_task['start'])[:-7], sub_task['start'], sub_task['end']))

        if task is None:
            for i, task in enumerate(self.tasks_status):
                for m, sub_task in enumerate(task):
                    if sub_task['end'] >= now >= sub_task['start']:
                        print_report('ON')
                    elif now <= sub_task['start'] or (now > sub_task['start'] and sub_task['end']):
                        print_report('OFF')
        else:
            sub_task = self.tasks_status[task[0]][task[1]]
            i, m = task[0], task[1]
            if sub_task['end'] >= now >= sub_task['start']:
                print_report('ON')
            elif now <= sub_task['start'] or (now > sub_task['start'] and sub_task['end']):
                print_report('OFF')


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


if __name__ == '__main__':
    def on_func():
        print('On function')


    def off_func():
        print('off function')


    # a = WifiControl()
    # a.read_pwd_fromfile()
    # a.wifi_on()

    b = RunWeeklySchedule(on_func=on_func, off_func=off_func, sched_file='sched1.txt')
    # b.add_weekly_task(new_task={'start_days': [6], 'start_time': '19:03:00', 'end_days': [6], 'end_time': '23:08:00'})
    # b.add_weekly_task(
    #     new_task={'start_days': [1, 6], 'start_time': '19:03:30', 'end_days': [1, 6], 'end_time': '19:03:40'})

    b.start()