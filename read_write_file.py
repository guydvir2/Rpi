import datetime
import time
import os
def time_diff(t1):
    t2 = datetime.datetime.now().time()
    today = datetime.date.today()
    return(datetime.datetime.combine(today, t1)-datetime.datetime.combine(today, t2))

tasks = ["08:44:00","14:00:01"]
t1=datetime.datetime.strptime(tasks[0],"%H:%M:%S").time()

#now=datetime.datetime.time()
# path = "C:\\Users\\guydvir\\PycharmProjects\\untitled\\"
# # time_str = datetime.datetime.now().strftime('%Y-%m-%d')
# fname = "timelog.txt"
# timelapse_minutes = 10
# hours = 1
#
# if os.path.isfile(path+fname):
#     print("file exists")
#     os.remove(path + fname)
#
# for t in range(1,int(hours*60/timelapse_minutes)+1):
#     file = open(path+fname, "a")
#     file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " >>" "Errlog #"+str(t)+ "\n")
#     file.close()
#     time.sleep(timelapse_minutes/10)
#
# file = open(path + fname, "r")
# print(file.read())
print(time_diff(t1).total_seconds())