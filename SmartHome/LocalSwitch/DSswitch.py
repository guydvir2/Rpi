from localswitches import HomePiLocalSwitch
import sys
import getopt
from time import sleep
import os

device_name='F-RoomWindow'
argv=sys.argv[1:]

if len(argv)>0:
    try:
        opts,args= getopt.getopt(argv,"u:d:s",["up=","down=","status="])
    except getopt.GetoptError:
        print ('-u<state> -d<state>')
        sys.exit(2)

    a=HomePiLocalSwitch(switch_type='double', gpio_in=[20, 21], gpio_out=[16, 26], mode='press',ext_log='/home/guy/Documents/%s.log'%(device_name), alias=device_name+'O/D')

    switch=''
    for opt, arg in opts:
        if opt == '-h':
            print ('-u --up -d --down, state=<on/off>')
            sys.exit(2)
        elif opt in ("-u", "--up"):
            switch = arg
            if arg == 'on' :
                a.switch.switch0.switch_state =1
            elif arg == "off":
                a.switch.switch0.switch_state =0
        elif opt in ("-d", "--down"):
            switch = arg
            if arg == 'on':
                a.switch.switch0.switch_state =1
            elif arg == "off":
                a.switch.switch1.switch_state =0
        elif opt in ("-s", "--status"):
            print(a.switch.switch0.switch_state)
    
            

else:

    loc_double_switch = HomePiLocalSwitch(switch_type='double', gpio_in=[20, 21], gpio_out=[16, 26], mode='press',ext_log='/home/guy/Documents/%s.log'%(device_name), alias=device_name)

    loc_double_switch.use_watch_dog()

    loc_double_switch.weekly_schedule(local_schedule_1={'start_days': [3], 'start_time': '19:03:00', 'end_days': [4], 'end_time': '23:08:00'}, sched_filename_1='/home/guy/Documents/github/Rpi/modules/sched1.txt')

    loc_double_switch.gmail_defs(recipients=['guydvir.tech@gmail.com'], sender_file='/home/guy/Documents/github/Rpi/modules/ufile.txt',password_file='/home/guy/Documents/github/Rpi/modules/pfile.txt')
