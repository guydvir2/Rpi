import datetime

now = ''

while True:
    now = str(datetime.datetime.now())[:-5]
    print(now)
