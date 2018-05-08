import cbit
import subprocess
import getip
from sys import platform
import datetime


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

    def __init__(self, func2run):
        self.tasks_status, self.weekly_tasks_list = [], []
        self.engage_task, self.on_tasks = [], None
        self.func2run = func2run
        self.cbit = cbit.CBit(500)
        """Engage flag gives the ability to enable or disable on/off regardless"""

    def add_weekly_task(self, new_task):
        self.weekly_tasks_list.append(new_task)
        # method indicates if start an active schedule
        self.engage_task.append([1] * len(new_task['start_days']))

    def run_once_week_sched(self, wtask):
        task_output_result = []
        # for loop in case of multiple days in task
        for i, day_task_start in enumerate(wtask['start_days']):
            status_dict = {}
            day_task_end = wtask['end_days'][i]
            status_dict['start'], status_dict['end'] = WeeklyIntervals(day_start=day_task_start,
                                                                       hour_start=wtask['start_time'],
                                                                       day_end=day_task_end,
                                                                       hour_end=wtask['end_time']).get_datetimes()
            if status_dict['start'] <= datetime.datetime.now() <= status_dict['end']:
                status_dict['state'] = 1
            else:
                status_dict['state'] = 0
            task_output_result.append(status_dict)
        return task_output_result

    def run_schedule(self):  # runs on cbit
        self.tasks_status = [[] for i in range(len(self.weekly_tasks_list))]

        def is_any_task_on():
            result = [None]
            for m, task in enumerate(self.tasks_status):
                for n, sub_task in enumerate(task):
                    if sub_task['state'] == 1:
                        if result == [None]:
                            result = [[m, n]]
                        else:
                            result.append([m, n])
            return result

        def is_task_engaged_and_on():
            on_tasks = is_any_task_on()
            result = []
            for on_task in on_tasks:
                try:
                    if self.tasks_status[on_task[0]][on_task[1]]['state'] == 1:
                        result.append(on_task)
                except TypeError:
                    # No Active tasks
                    pass
            return result

        def inject_tasks_to_schedule():
            self.tasks_status = list(map(self.run_once_week_sched, self.weekly_tasks_list))
            get_on_tasks()

        def get_on_tasks():
            # two conditions to flag "ON" state: 1) inside time window on/off. 2)engage flag is "ON"
            on_and_engaged = is_task_engaged_and_on()
            self.on_tasks = list(map(lambda list_1: self.tasks_status[list_1[0]][list_1[1]], on_and_engaged))
            self.run_func()
            # self.get_all_tasks_report()
            # get_start_times = list(map(lambda list_1: list_1['start'], self.on_tasks))
            # get_off_times = list(map(lambda list_1: list_1['end'], self.on_tasks))
            # get_durations = list(map(lambda list_1: list_1['end'] - list_1['start'], self.on_tasks))
            # print(get_start_times[0], get_off_times[0], get_durations[0])

        self.cbit.append_process(inject_tasks_to_schedule)
        self.cbit.init_thread()

    def run_func(self):
        for i, on_task in enumerate(self.on_tasks):
            now = datetime.datetime.now()
            self.func2run()
            get_start_times = list(map(lambda list_1: list_1['start'], self.on_tasks))
            get_off_times = list(map(lambda list_1: list_1['end'], self.on_tasks))
            print('[' + str(now)[:-5] + ']',
                  "task #%d start:%s, left:%s" % (i, get_start_times[i], get_off_times[i] - now))

    def get_all_tasks_report(self):
        now = datetime.datetime.now()
        for i, task in enumerate(self.tasks_status):
            for m, sub_task in enumerate(task):
                if sub_task['end'] >= now >= sub_task['start']:
                    print('Task #%d/%d:[ON:%s], start:[%s], end:[%s]' % (
                        i, m, str(now - sub_task['start'])[:-7], sub_task['start'], sub_task['end']))
                elif now <= sub_task['start'] or (now > sub_task['start'] and sub_task['end']):
                    print('Task #%d/%d:[OFF: %s], start:[%s], end:[%s]' % (
                        i, m, str(now - sub_task['end'])[:-7], sub_task['start'], sub_task['end']))

    def get_on_tasks(self):
        return self.on_tasks

    def get_raw_status(self):
        return self.tasks_status


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
    def my_func():
        print('Im On')


    # a = WifiControl()
    # a.read_pwd_fromfile()
    # a.wifi_on()

    b = RunWeeklySchedule(func2run=my_func)
    b.add_weekly_task(
        new_task={'start_days': [1, 2], 'start_time': '15:30:00', 'end_days': [1, 3], 'end_time': '20:01:27'})
    b.add_weekly_task(new_task={'start_days': [3], 'start_time': '20:02:00', 'end_days': [3], 'end_time': '20:03:00'})
    b.run_schedule()
