import datetime


def day_shift_time_tuple(delta_days, time):
    """create a datetime tuple of shifted day- days and clock"""
    clock_format = '%H:%M:%S'
    clock = datetime.datetime.strptime(time, clock_format)

    shifted_datetime = datetime.datetime.combine(
        datetime.datetime.now().date() + datetime.timedelta(days=delta_days), clock.time())
    return shifted_datetime


def shift_from_toady_time_tuple(day, hour):
    shifted_datetime = day_shift_time_tuple(day - iso2h_day_convert(datetime.datetime.now().isoweekday()), hour)
    return shifted_datetime


def iso2h_day_convert(iso_day):
    if 1 <= iso_day <= 6:
        day = iso_day + 1
    elif iso_day == 7:
        day = 1
    else:
        day = None
    return day


def h2iso_convert_day(day):
    if 2 <= day <= 7:
        iso_day = day - 1
    elif day == 1:
        iso_day = 7
    return iso_day


# def delta_days(iso_day1, iso_day2):
#     delt_d = iso2h_day_convert(iso_day2) - iso2h_day_convert(iso_day1)
#     if delt_d < 0:
#         delt_d += 7
#     return delt_d


# print(delta_days(1,3))

# now = datetime.datetime.now()
# today_day = iso2h_day_convert(now.isoweekday())
# today_hour = now.time()
# clock_format = '%H:%M:%S'

start_day = 7
end_day = 6
start_hour = "13:00:10"
end_hour = "11:00:00"

# start_hour = datetime.datetime.strptime('12:00:00', clock_format)
# end_hour = datetime.datetime.strptime('17:00:00', clock_format)

# print(day_shift_time_tuple(2, '14:00:00'))

# scenario A
start_datetime = shift_from_toady_time_tuple(start_day, start_hour)
if end_day - start_day >= 0:
    # start_datetime = shift_from_toady_time_tuple(start_day, start_hour)
    end_datetime = shift_from_toady_time_tuple(end_day, end_hour)
else:
    end_datetime = shift_from_toady_time_tuple(end_day + 7, end_hour)

if start_datetime > end_datetime:
    end_datetime +=datetime.timedelta(days=7)
    print("BAAAA")
    #
    # if start_day >= today_day:
    #     start_datetime = shift_from_toady_time_tuple(start_day, start_hour)
    #     end_datetime = shift_from_toady_time_tuple(end_day+7, end_hour)
    # elif start_day < today_day:
    #     start_datetime = shift_from_toady_time_tuple(start_day, start_hour)
    #     end_datetime = shift_from_toady_time_tuple(end_day + 7, end_hour)

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
