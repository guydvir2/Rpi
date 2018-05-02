import datetime

now = datetime.datetime.now()
today_day = now.isoweekday()
today_hour = now.time()
clock_format = '%H:%M:%S'

# print(datetime.datetime.isocalendar())
days = [None, 7, 1, 2, 3, 4, 5, 6]
start_day = 1
end_day = 6
start_hour = datetime.datetime.strptime('12:00:00', clock_format)
end_hour = datetime.datetime.strptime('17:00:00', clock_format)

if days[end_day] - today_day < 0 and days[start_day] - today_day < 0:
    end_day_corrected = days[end_day] + 7
else:
    end_day_corrected = end_day

start_datetime = datetime.datetime.combine(
    datetime.datetime.now().date() + datetime.timedelta(days=days[start_day] - today_day), start_hour.time())
end_datetime = datetime.datetime.combine(
    datetime.datetime.now().date() + datetime.timedelta(days=days[end_day] - today_day), end_hour.time())

print(start_datetime, end_datetime)
