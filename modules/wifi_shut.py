import cbit
import subprocess
import getip
from sys import platform
import datetime


class WeekTimeInterval:
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

    def h2iso_convert_day(self, ay):
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

        if start_datetime > end_datetime:
            end_datetime += datetime.timedelta(days=7)
        return start_datetime, end_datetime


class Time2Start:
    def __init__(self):
        self.tasks_status, self.weekly_tasks_list = [], []
        self.clock_format = '%H:%M:%S'
        self.date_format = '%Y-%m-%d'
        self.cbit = cbit.CBit(500)
        self.engage_task = []

    def swipe_weekly_schedule(self, wtask):
        task_output_result = []
        # for loop for multiple days in task

        for i, day_task_start in enumerate(wtask['start_days']):
            status_dict = {}
            day_task_end = wtask['end_days'][i]
            status_dict['start'], status_dict['end'] = WeekTimeInterval(day_start=day_task_start,
                                                                        hour_start=wtask['start_time'],
                                                                        day_end=day_task_end,
                                                                        hour_end=wtask['end_time']).get_datetimes()
            if status_dict['start'] <= datetime.datetime.now() <= status_dict['end']:
                status_dict['state'] = 1

            else:
                status_dict['state'] = 0

            #     timenow = self.time_now()
            #     delta_time_start = datetime.datetime.combine(timenow.date(),
            #                                                  datetime.datetime.strptime(wtask['start_time'],
            #                                                                             self.clock_format).time()) - timenow
            #     delta_time_end = datetime.datetime.combine(timenow.date(),
            #                                                datetime.datetime.strptime(wtask['end_time'],
            #                                                                           self.clock_format).time()) - datetime.datetime.combine(
            #         timenow.date(),
            #         datetime.datetime.strptime(wtask['start_time'], self.clock_format).time())
            #
            #     delta_days_start = day_task_start - timenow.isoweekday()
            #     if delta_days_start < 0:
            #         delta_days_start += 7
            #     time_to_start = datetime.timedelta(days=delta_days_start) + delta_time_start
            #
            #     delta_days_end = day_task_end - day_task_start
            #     if delta_days_end < 0:
            #         delta_days_end += 7
            #     time_to_end = datetime.timedelta(days=delta_days_end) + delta_time_end + time_to_start
            #
            #     status_dict['start'] = time_to_start
            #     status_dict["end"] = time_to_end
            #     if time_to_start.total_seconds() < 0:
            #         if time_to_end.total_seconds() > 0:
            #             status_dict['state'] = 1
            #     else:
            #         status_dict['state'] = 0
            #     task_output_result.append(status_dict)
            #
            # return task_output_result
            task_output_result.append(status_dict)
            print(task_output_result)

    def exec_tasks_run(self):
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
            print(result)
            return result

        def is_task_engaged_and_on():
            on_tasks = is_any_task_on()
            result = []
            for on_task in on_tasks:
                if self.tasks_status[on_task[0]][on_task[1]]['state'] == 1:
                    result.append(on_task)
            return result

        def inject_tasks_to_schedule():
            self.tasks_status = list(map(self.swipe_weekly_schedule, self.weekly_tasks_list))
            print(self.tasks_status)
            # is_any_task_on()
            # print(is_task_engaged_and_on())

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
        # method indicates if start an active schedule
        self.engage_task.append([1] * len(new_task['start_days']))

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
b.add_weekly_task(new_task={'start_days': [1, 4], 'start_time': '11:30:00', 'end_days': [5, 6], 'end_time': '22:00:00'})
b.add_weekly_task(new_task={'start_days': [3], 'start_time': '07:30:00', 'end_days': [3], 'end_time': '22:35:00'})
#
b.exec_tasks_run()
