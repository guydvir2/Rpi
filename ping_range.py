import os

list_found=[]
for i in range(100,140):
    print("address:",i)
    adress='192.168.2.'+str(i)
    ping_result = os.system('ping %s -c 1' %adress)
    if ping_result == 0:
        list_found.append(adress)

print(list_found)
