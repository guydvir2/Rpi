import csv
import datetime


input_file="myfile2.csv"
# data = ["value %d" % i for i in range(1,4)]
data = ["task no.", "device no.","uptime", "downtime", str(datetime.datetime.now())]
out = csv.writer(open(input_file , "w"), delimiter=',',quoting=csv.QUOTE_ALL)
out.writerow(data)

print(datetime.datetime.now())

# import csv
rows=[]
o=0


with open(input_file, newline='') as f:
    reader = csv.reader(f, delimiter=',' , quoting=csv.QUOTE_ALL)
    for m in reader:
        print(m)

