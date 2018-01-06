from array import array
import numpy
from math import *
from pylab import plot, show
import datetime
from random import randrange, uniform
import time



samples=[[]]
t=0
while t<5:
    try:
        print("T=",t)
        samples[0].append(str(t)+") "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" ->"+str(round(uniform(0,10)/10*1000)))
        #samples[1].append(round(uniform(0,10)/10*1000))
        t +=1
        time.sleep(2)
    except KeyboardInterrupt:
        print("shit")

print(samples)

b=numpy.array(samples)
print(b.shape)
#print(b[:,0:])
print(b)
# for v in range(len(b[0])):
#     print(b[:,v])



# linsp=numpy.linspace(0,2*pi,1000)
# x=0
# for i in linsp:
#     a[1].append(sin(i))
#     a[0].append(cos(i))

#print(len(a[0]))
#plot(linsp/pi,a[1])
#plot(linsp/pi,a[0])
#show()
#print(datetime.datetime.now())