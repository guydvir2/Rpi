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

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1, 6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/window1_up':
        win1_commands(0,1)
        bot.sendMessage(chat_id, 'Window 1 set UP')
    elif command == '/window1_down':
        win1_commands(1,1)
        bot.sendMessage(chat_id, 'Window 1 set DOWN')
    elif command == '/window1_stop':
        win1_commands(1,0)
        bot.sendMessage(chat_id, 'Window 1 stopped')
        
    else:
        bot.sendMessage(chat_id, 'pppfff comme on')

def win1_commands(direction,state):
    win1.set_state(0, 0)
    win1.set_state(1, 0)
    print(win1.get_state())
    win1.set_state(direction,state)
    print(win1.get_state())
    #a.close_device()

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
from gpiobuttonlib import HWRemoteOutput

root = tk.Tk()
chat_id = 596123373
build_gui(root)
bot = telepot.Bot('497268459:AAFrPh-toL6DPPArWknqJzIAby8jMi21S4c')
me = bot.getMe()
root.title('Telegram BOT:' +me['first_name'] + '#' + str(me['id']))
win1 = HWRemoteOutput(ip='192.168.2.114', output_pins=[19,26],switch_type='press')
MessageLoop(bot, handle).run_as_thread()

root.mainloop()
#
# while 1:
#     time.sleep(10)
