import datetime


def create_datetime(delta_days, time):
    clock_format = '%H:%M:%S'
    # today_day = datetime.datetime.now().isoweekday()
    clock = datetime.datetime.strptime(time, clock_format)
    start_datetime = datetime.datetime.combine(
        datetime.datetime.now().date() + datetime.timedelta(days=delta_days), clock.time())
    return start_datetime


def decide_dates(day, hour):
    today_day = convert_iso_days(now.isoweekday())
    delt_days = day - today_day
    if delt_days < 0:
        start_datetime = create_datetime(delt_days, hour)
    else:
        start_datetime = create_datetime(-delt_days, hour)
    return start_datetime


def convert_iso_days(iso_day):
    if 1 <= iso_day <= 6:
        day = iso_day + 1
    elif iso_day == 7:
        day = 1
    else:
        day = None
    return day


def convert_toiso_day(day):
    if 2 <= day <= 7:
        iso_day = day - 1
    elif day == 1:
        iso_day = 7
    return iso_day


def delta_days(iso_day1, iso_day2):
    delt_d = convert_iso_days(iso_day2) - convert_iso_days(iso_day1)
    if delt_d < 0:
        delt_d += 7
    return delt_d


# print(delta_days(1,3))

# print(datetime.datetime.isocalendar())

now = datetime.datetime.now()
today_day = convert_iso_days(now.isoweekday())
today_hour = now.time()
clock_format = '%H:%M:%S'

start_day = 1
end_day = 6
start_hour = "12:00:10"
end_hour = "17:00:00"

# start_hour = datetime.datetime.strptime('12:00:00', clock_format)
# end_hour = datetime.datetime.strptime('17:00:00', clock_format)

# print(create_datetime(2, '14:00:00'))

# scenario A
if end_day - start_day > 0:
    start_datetime = decide_dates(start_day, start_hour)
    end_datetime = decide_dates(end_day, end_hour)

    print(start_datetime, end_datetime)

#
#
# if days[end_day] - today_day < 0 and days[start_day] - today_day < 0:
#     end_day_corrected = days[end_day] + 7
# else:
#     end_day_corrected = end_day
#
# start_datetime = datetime.datetime.combine(
#     datetime.datetime.now().date() + datetime.timedelta(days=days[start_day] - today_day), start_hour.time())
# end_datetime = datetime.datetime.combine(
#     datetime.datetime.now().date() + datetime.timedelta(days=days[end_day] - today_day), end_hour.time())
#
# print(start_datetime, end_datetime)
