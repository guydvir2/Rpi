import ButtonLib2
import readfile_ssh
import tablegui
import tkinter as tk
from tkinter import ttk

import datetime
import numpy as np
from sys import platform


class ButtonsGUI(ttk.Frame):
    """AllButtons GUI Class"""

    def __init__(self, master, mainframe):

        self.master = master
        self.mframe = mainframe
        ttk.Frame.__init__(self, master)
        self.reachable_ips = ['192.168.2.115', '192.168.2.113']
        self.master.write2log("Valid IP's to load:" + str(self.reachable_ips))
        self.args = []  # Dictionary of loaded buttons definitions, KWargs for
        # GUIButtons Read But Defs from file

        self.buts = []
        self.reload_all()

    def prep_buttons(self):
        # self.reload_data_files()
        # self.list_buts_to_load()
        # self.checkFalse_err()
        self.reload_data_files()
        self.load_buttons_defs()
        self.get_sched_defs()

    def reload_all(self):
        self.mainframe = ttk.LabelFrame(self.mframe, text="Button")
        self.mainframe.grid(padx=5, pady=5)

        self.loaded_buts, self.sched_vector, self.but2load = [], [], []

        self.prep_buttons()
        self.build_gui()

    def reload_data_files(self):
        self.master.FileManButs.save_to_file(mat=self.master.ButConfigTable.
                                             extract_data())
        self.master.read_data_from_files()

    def load_buttons_defs(self):

        # keys "hw_in","hw_out","dimension" - get special treatment in next for
        # loop in extracting string values
        self.button_keys = ['id', 'on_off', 'type', 'nickname', 'ip_out', 'hw_out', 'hw_in',
                            'ip_in', 'dimension']

        start_key = 1
        for i, but_defs in enumerate(self.master.buts_defs):
            c, t = {}, start_key
            for m in self.button_keys[start_key:7]:

                # fields that get more than one parameter
                if m == 'hw_out' or m == 'hw_in':
                    c[m] = self.master.xtrct_nums(but_defs[t])
                elif m == 'dimension':
                    if not but_defs[t] == '':
                        if not self.master.xtrct_nums(but_defs[t])[1] == []:
                            c['height'] = self.master.xtrct_nums(but_defs[t])[1]
                        else:
                            c['height'] = ''
                        if not self.master.xtrct_nums(but_defs[t])[0] == []:
                            c['width'] = self.master.xtrct_nums(but_defs[t])[0]
                        else:
                            c['width'] = ''
                    else:
                        pass
                else:
                    # All other keys which are not "special":
                    c[m] = but_defs[t]
                t += 1

            # a dict contains all argument needed to define a button
            del c['type']
            self.args.append(c)

    def get_sched_defs(self):

        # Import sched file to define button's sched
        dev_names = []  # Alias of device
        off_list = []  # items that are OFF in TimeTable GUI
        for i, current_task in enumerate(self.master.sched_file):
            # Note : the following if statement- checks if task is selected to run ( via t.table gui ), aka 1 is checked
            # for run. now it is selected as to to bypass this if statemnet. i think at the momnet is is not a valid
            # checc
            if current_task[1] == "0" or not all(current_task[0:6]):
                off_list.append(i)
            self.sched_vector.append(current_task[3:6])
            self.sched_vector[i][0] = self.master.xtrct_nums(current_task[3])
            dev_names.append(current_task[2])
        # Create a list- including buttons and ALL sched in sched_vector ( multilpe values)
        self.device_list_sched = []  # this list contain index of buttons in sched list
        for x, dev in enumerate(list(set(dev_names))):
            self.device_list_sched.append([dev])  # name of device
            self.device_list_sched[x].append([])  # index
            self.device_list_sched[x].append([])  # sched_vector

            for i, u in enumerate(self.master.sched_file):
                if dev in u and i not in off_list:
                    self.device_list_sched[x][1].append(i)
                    self.device_list_sched[x][2].append(self.sched_vector[i])

        # Update sched_vector into self.args
        for i, args in enumerate(self.args):
            for t, sched in enumerate(self.device_list_sched):
                if args['nickname'] == sched[0] or args['nickname'] in sched[0] and '[DOWN]' in sched[0].upper():
                    self.args[i]['sched_vector'] = self.device_list_sched[t][2]
                elif args['nickname'] in sched[0] and '[UP]' in sched[0].upper():  # Valid to Window UP sched
                    self.args[i]['sched_vector2'] = self.device_list_sched[t][2]

    def build_gui(self):

        x = 0
        for l, current_button in enumerate(self.master.buts_defs):
            try:
                # load button if it in allowed ip list and not off in table
                # [ 'No','Type','nick','ip_out','hw_out','hw_in','on/off']
                if current_button[4] in self.reachable_ips:
                    self.buts.append(getattr(ButtonLib2, current_button[2])
                                     (self.mainframe, **self.args[l]))
                    self.loaded_buts.append([x, self.args[l]['nickname']])
                    self.buts[x].grid(row=0, column=x)
                    x += 1

            except ValueError:
                self.master.write2log("Error loading Button" + str(l))
        self.master.write2log("Buttons loaded successfully: " + str([x[1] for x in self.loaded_buts]))

    def close_for_reload(self):
        for but in self.buts:
            but.close_all()
        self.mainframe.destroy()

        self.master.write2log("Shutting all buttons...Done!")

    def update_schedule(self):

        self.prep_buttons()
        x = 2
        self.buts[x].close_all()
        self.buts[x] = getattr(ButtonLib2, self.master.buts_defs[x][1])\
            (self.mainframe, **self.args[int(self.master.buts_defs[x][0])])
        self.buts[x].grid(row=0, column=x)


class MainGUI(ttk.Frame):
    """ This MainGui Class"""

    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Get OS type - and select path
        os_type = platform
        if os_type == 'darwin':
            self.path = '/Users/guy/Documents/gitHub/Rpi/SmartHome/'
        elif os_type == 'win32':
            self.path = 'd:/users/guydvir/Documents/git/Rpi/SmartHome/'
        elif os_type == 'linux':
            self.path = '/home/guy/Documents/gitHub/Rpi/SmartHome/'

        # self.path = '/home/guy/PythonProjects/SmartHome/'

        self.but_filename = 'ButtonsDef2.csv'
        self.sched_filename = 'Schedule.csv'
        self.app_name = 'Pi Scheduler'
        master.title(self.app_name)

        self.reload_all()

    def reload_all(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid()

        self.connected_devices, self.sched_vector = [], []

        self.read_data_from_files()
        self.build_gui()

    def read_data_from_files(self):
        self.FileManButs = readfile_ssh.LoadFile(filename=self.but_filename, path=self.path)
        self.buts_defs = self.FileManButs.data_from_file

        self.FileManSched = readfile_ssh.LoadFile(filename=self.sched_filename, path=self.path)
        self.sched_file = self.FileManSched.data_from_file

    def save_data_to_file(self):
        self.FileManButs.save_to_file(mat=self.ButConfigTable.extract_data_from_gui())
        self.FileManSched.save_to_file(mat=self.WeekSched_TimeTable.extract_data_from_gui())

    def close_for_reload(self):
        self.ButtonNote.close_for_reload()
        self.main_frame.destroy()
        self.reload_all()

    def build_gui(self):
        notebook = ttk.Notebook(self.main_frame)

        self.sched_tab = ttk.Frame(notebook)
        self.config_but_tab = ttk.Frame(notebook)
        self.buttons_tab = ttk.Frame(notebook)
        self.activity_log_tab = ttk.Frame(notebook)

        notebook.add(self.sched_tab, text="Weekly Schedule", compound=tk.TOP)
        notebook.add(self.buttons_tab, text="Buttons", compound=tk.TOP)
        notebook.add(self.config_but_tab, text="Hardware Config", compound=tk.TOP)
        notebook.add(self.activity_log_tab, text="Activity Log", compound=tk.TOP)
        notebook.grid()

        self.log_window()
        self.write2log("Boot")
        self.butt_config_gui(2, 0)
        self.buttons_gui(1, 0)
        self.weekly_sched_gui(0, 0)

    def weekly_sched_gui(self, r=0, c=0):
        def name_no_br(name):
            ret_name, ext = None, None

            if '[' in name:
                ret_name = name[:name.index('[')]
                ext = name[name.index('['):]
            else:
                ret_name = name

            return [ret_name, ext]



        def print_timetable():
            total_V = []
            m = np.array(self.WeekSched_TimeTable.extract_data())

            # for i, sched in enumerate(m):
            #     v = [[], [], []]
            #
            #     if '[UP]' in sched[2].upper():
            #         v[0] = sched[2][:sched[2].index('[')]
            #         v[2] = [sched[3:6]]
            #     elif '[DOWN]' in sched[2].upper():
            #         v[0] = sched[2][:sched[2].index('[')]
            #         v[1] = [sched[3:6]]
            #     else:
            #         v[0] = sched[2]
            #         v[1] = [sched[3:6]]
            #
            #     total_V.append(v)
            # print(total_V)

        devices_names = []
        # import configured devices names into timetable
        for dev in self.buts_defs:
            if dev[2] == 'UpDownButton':
                devices_names.append(dev[3] + '[Up]')
                devices_names.append(dev[3] + '[Down]')
            else:
                devices_names.append(dev[3])

        self.WeekSched_TimeTable = tablegui.TimeTableConfigGUI(self.sched_tab,
                                                               data_file_name=self.path + self.sched_filename,
                                                               list=devices_names)
        self.WeekSched_TimeTable.grid(row=r, column=c)
        self.write2log("Weekly schedule GUI started")

        ttk.Button(self.sched_tab, text='reload schedule', command=self.ButtonNote.update_schedule).grid()

    def butt_config_gui(self, r=0, c=0):

        buttons_type = getattr(ButtonLib2, 'button_list')  # Get Button type from ButtonLib
        self.ButConfigTable = tablegui.DeviceConfigGUI(self.config_but_tab,
                                                       data_file_name=self.path + self.but_filename,
                                                       list=buttons_type)
        self.ButConfigTable.grid(row=r, column=c)
        self.write2log("Buttons config GUI loaded")

    def buttons_gui(self, r=0, c=0):

        self.ButtonNote = ButtonsGUI(self, self.buttons_tab)
        self.ButtonNote.grid(row=0, column=0)

        self.write2log("Buttons GUI loaded")

    def log_window(self):
        # Create log Tab
        self.text_tab = tk.Text(self.activity_log_tab, width=100, height=16, bg='snow4')
        self.text_tab.grid(row=0, column=0, sticky=tk.E + tk.W)
        scrollbar = ttk.Scrollbar(self.activity_log_tab)
        scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)
        scrollbar.config(command=self.text_tab.yview)
        self.text_tab.config(yscrollcommand=scrollbar.set)
        self.text_tab.config(state=tk.DISABLED)

        log_button = ttk.Button(self.activity_log_tab, text="Save log")  # , command=self.save_log)
        log_button.grid(row=1, column=0, sticky=tk.E, pady=10)

    def write2log(self, text_in):
        self.text_tab.config(state=tk.NORMAL)
        time2log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        start = tk.END
        self.text_tab.insert(start, "[" + str(time2log) + "] " + text_in + "\n")
        self.text_tab.config(state=tk.DISABLED)

    def xtrct_nums(self, lista):
        # make a list from str or list comb iwth strings
        new_list = []

        def xtrct_str(listb):
            new_lst = []
            temp = ''

            for i in range(len(listb)):
                try:
                    int(listb[i])  # try in int
                    temp = temp + listb[i]  # use is as char !
                except ValueError:
                    if not temp == '':
                        new_lst.append(int(temp))
                        temp = ''
                # for last number in str
                if i == len(listb) - 1 and not temp == '':
                    new_lst.append(int(temp))

            return new_lst

        if type(lista) is str:
            new_list = xtrct_str(lista)

        elif type(lista) is list:
            for item in lista:
                if type(item) is int:
                    new_list.append(item)
                elif type(item).__name__ == 'str':
                    z = xtrct_str(item)
                    if not z == []: new_list.append(xtrct_str(item)[0])

        return new_list

    def findtasknum(self, m):
        sch_num = None
        task_num = list(np.array(self.sched_file)[:m + 1, 2]).count(self.sched_file[m][2])
        if '[UP]' in self.sched_file[m][2].upper():
            sch_num = 1
        else:
            sch_num = 0
        if '[' in self.sched_file[m][2]:
            i = self.sched_file[m][2].index('[')
            name = self.sched_file[m][2][:i]
        else:
            name = self.sched_file[m][2]

        return [task_num - 1, sch_num, name]


root = tk.Tk()

app = MainGUI(root)
app.grid()

root.mainloop()
