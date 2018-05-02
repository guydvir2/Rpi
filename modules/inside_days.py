import datetime

now = datetime.datetime.now()
today_day = now.isoweekday()
today_hour = now.time()
clock_format = '%H:%M:%S'

start_day = 2
end_day = 2
datetime.datetime.strptime('12:00:00', clock_format)
start_hour = datetime.datetime.strptime('12:00:00', clock_format)
end_hour = datetime.datetime.strptime('17:00:00', clock_format)

if end_day - start_day < 0:
    end_day_corrected = end_day + 7
else:
    end_day_corrected = end_day

start_datetime = datetime.datetime.combine(
    datetime.datetime.now().date() + datetime.timedelta(days=start_day - today_day), start_hour.time())
end_datetime = datetime.datetime.combine(
    datetime.datetime.now().date() + datetime.timedelta(days=end_day_corrected - today_day), end_hour.time())

print(start_datetime, end_datetime)
