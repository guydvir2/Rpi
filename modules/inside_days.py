import datetime

now = datetime.datetime.now()
today_day = now.isoweekday()
today_hour = now.time()

start_day = 3
end_day = 0
start_hour = now.time()
end_hour = now.time()

if end_day - start_day < 0:
    end_day_corrected = end_day + 7
else:
    end_day_corrected = end_day

start_datetime = now + datetime.timedelta(days=start_day - today_day)
end_datetime = now + datetime.timedelta(days=end_day_corrected - today_day)

print(start_datetime, end_datetime)
