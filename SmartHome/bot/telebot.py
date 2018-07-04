import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
import tkinter as tk
from sys import platform, path

"""
- `/roll` - reply with a random integer between 1 and 6, like rolling a dice.
- `/time` - reply with the current time, like a clock.
"""


def build_gui(frame):
    global log1

    def send_text():
        bot.sendMessage(chat_id, text_input.get())
        put_log('bot: %s'% str(text_input.get()))
        text_input.set('')

    frame1 = tk.Frame(frame)
    frame1.grid()
    frame2 = tk.Frame(frame)
    frame2.grid(row=1, column=0)

    text_input = tk.StringVar()
    msg_entry = tk.Entry(frame1, textvariable=text_input)
    msg_entry.grid(row=0, column=0)
    send_btn = tk.Button(frame1, text='Send', command=send_text)
    send_btn.grid(row=0, column=1)
    label1 = tk.Label(frame2, text='BOT log')
    label1.grid(row=0, column=0, sticky=tk.W)
    log1 = tk.Text(frame2, height=15, width=50, wrap=tk.NONE, bd=1, relief=tk.RIDGE)
    log1.grid(row=1, column=0)
    log1.insert(tk.END, "BOT log:\n")


def put_log(msg):
    global log1
    log1.insert(tk.END, msg + '\n')


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    put_log('%s %s: %s' % (msg['from']['first_name'], msg['from']['last_name'], command))

    if command == '/window1_up':
        win1_commands(0,1)
        msg='Window 1 set UP'
        #bot.sendMessage(chat_id, 'Window 1 set UP')
    elif command == '/window1_down':
        win1_commands(1,1)
        msg='Window 1 set DOWN'
    elif command == '/window1_stop':
        win1_commands(1,0)
        msg='Window 1 stopped'
    elif command == '/alarm_home_arm':
        alarm_system_commands(1,1)
        msg='Alarm System: Home Mode is ON'
    elif command == '/alarm_home_disarm':
        alarm_system_commands(1,0)
        msg='Alarm System: Home Mode is OFF'
    elif command == '/alarm_full_arm':
        alarm_system_commands(0,1)
        msg = 'Alarm System: Full Mode is ON'
    elif command == '/alarm_full_disarm':
        alarm_system_commands(0,0)
        msg='Alarm System: Full Mode is OFF'
    
    elif command == '/alarm_status':
        t=alarm_system_ind_commands()
        msg='Alarm System ARMED: %s\nSystem is Alarming: %s'%(t[1], t[0])
        
    else:
        msg='Unknown command'
    
    bot.sendMessage(chat_id, msg)
    put_log('bot: %s'%msg)
        

def win1_commands(direction,state):
    win1.set_state(0, 0)
    win1.set_state(1, 0)
    win1.set_state(direction,state)
    
def alarm_system_commands(mode, state):
    # mode = 1 : Home Arm
    # mode = 0 : Full
    
    if state == 1:
        alarm_system.set_state(mode,state)
    elif state == 0:
        alarm_system.set_state(mode,state)

def alarm_system_ind_commands():
    # mode = 1 : Home Arm
    # mode = 0 : Full
    return alarm_system_indicators.get_state()

os_type = platform
if os_type == 'darwin':
    main_path = '/Users/guy/Documents/github/Rpi/'
elif os_type == 'win32':
    main_path = 'd:/users/guydvir/Documents/git/Rpi/'
elif os_type == 'linux':
    main_path = '/home/guy/Documents/github/Rpi/'

path.append(main_path + 'GPIO_Projects/lcd')
path.append(main_path + 'SmartHome/LocalSwitch')
path.append(main_path + 'modules')
path.append(main_path + 'SmartHome/LocalSwitch')
path.append(main_path + 'SmartHome/RemoteSwitch')
from gpiobuttonlib import HWRemoteOutput, HWRemoteInput

root = tk.Tk()
chat_id = 596123373
build_gui(root)
bot = telepot.Bot('497268459:AAFrPh-toL6DPPArWknqJzIAby8jMi21S4c')
me = bot.getMe()
root.title('Telegram BOT:' +me['first_name'] + '#' + str(me['id']))

win1 = HWRemoteOutput(ip='192.168.2.114', output_pins=[19,26],switch_type='press')
alarm_system = HWRemoteOutput(ip='192.168.2.117', output_pins=[16,26],switch_type='press')
alarm_system_indicators = HWRemoteInput(ip='192.168.2.117', input_pins=[20,21],switch_mode='toggle')

alarm_system_ind_commands()

MessageLoop(bot, handle).run_as_thread()
root.mainloop()
#
# while 1:
#     time.sleep(10)
