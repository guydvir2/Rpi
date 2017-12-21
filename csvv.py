
import csv
import datetime
from sys import platform

if platform == 'linux':
    file3 = "/home/guy/PythonProjects/schedule.csv"
elif platform == 'darwin':
    file3 = "/Volumes/Guy/PythonProjects/guy.csv"
elif platform == 'win32':
    file3 = "d:\\guy.csv"
         
        
     

def write_csv(file3,list1,p):
    outputfile=open(file3,p,newline="")
    outputwriter = csv.writer(outputfile)#, dialect='excel')
    outputwriter.writerows(list1)
    outputfile.close()

def read_csv(file3):
    with open(file3, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        return your_list

headers=["Task No.","Enable/Disable","Week Days","Start Time","Finish Time",'Device No.']
intake_task1=["1","on",[6],"23:07:00","01:08:00","1"]
intake_task2=["2","on",[1,7,2],"16:25:00","16:27:00","1"]
intake_task3=["3","on",[1,3,5,7,2,4,6],"11:57:00","11:58:30","1"]
intake_task4=["4","off",[1,3,2,4,6],"17:45:00","17:46:00","2"]
intake_task5=["5","on",[1,3,6,2],"21:57:00","21:58:00","1"]

write_csv(file3,[headers,intake_task1,intake_task2,intake_task3,intake_task4,intake_task5],'w')

#list1=read_csv(file3)
#print((list1))
#for b in range(len(list1)):
    #print(list1[b])

