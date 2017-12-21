import datetime
import tkinter
import time
from tkinter import ttk

class ScheduledEvents:
    
    def __init__(self, tasks):
        self.tasks = tasks
        self.result_vector, self.future_on = [0] * len(self.tasks), [0] * len(self.tasks)

        if self.check_integrity_time_table() == 0:
            self.run_schedule()

        else:
            print("Errors in TimeTable")


    def check_integrity_time_table(self):
        time_err, days_err = 0, 0
        
        for i in range(len(self.tasks)):
            print(self.tasks[i])
            time1 = datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time()
            time2 = datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time()
            
            for day_in_task in self.tasks[i][0]:
                if not day_in_task in range(1, 8):
                    print("day of task %d is not valid" % i)
                    days_err += 1

                if not time2 > time1:
                    print("Time interval of task %d is not valid" % i)
                    time_err += 1

        if time_err + days_err == 0:
            return 0  # No Errors
        else:
            return 1  # Errors on TimeTable


    def run_schedule(self):      
        
        def time_diff(t1):
            t2 = datetime.datetime.now().time()
            today1 = datetime.date.today()
            return datetime.datetime.combine(today1, t1) - datetime.datetime.combine(today1, t2)

        def chop_microseconds(delta):
            return delta - datetime.timedelta(microseconds=delta.microseconds)


        for i in range(len(self.tasks)):
            self.result_vector[i] = [2]*len(self.tasks[i][0])
            self.future_on[i] = [2]*len(self.tasks[i][0])
            
        for i in range(len(self.tasks)): #Total tasks
            for m,day_in_task in enumerate(self.tasks[i][0]): #days in same task
                day_diff = day_in_task - datetime.datetime.today().isoweekday()

                #Today
                if day_in_task == datetime.date.today().isoweekday():
                    start_time = datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time()
                    stop_time = datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time()

                    #Before Time
                    if start_time > datetime.datetime.now().time():
                        self.result_vector[i][m] = -1
                        
                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(day_diff), datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())
                        #print("b4")


                    #In Time
                    elif start_time  < (datetime.datetime.now()-datetime.timedelta(seconds=1)).time() and (datetime.datetime.now() + datetime.timedelta(seconds=1)).time() < stop_time:
                        self.result_vector[i][m] = 1
                        
                        new_date = datetime.datetime.combine(datetime.date.today() , datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time())
                        #print("innnn")

                    #Time to Off
                    elif (datetime.datetime.now()+datetime.timedelta(seconds=2)).time() >stop_time and datetime.datetime.now().time() < stop_time  :
                        self.result_vector[i][m] = 0
                        #print("offff")

                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7) , datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())

                    # Byond Command Times
                    else :
                        self.result_vector[i][m] = -1
                        
                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7) , datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())



                #Day in Future
                elif day_in_task > datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1
                    
                    new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta
                    (day_diff), datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())
                    

                #Day in Past, Next in Future
                elif day_in_task < datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1
                    
                    new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7+day_diff), datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())

                self.future_on[i][m] = str(chop_microseconds(new_date - datetime.datetime.now()))


    def get_status(self):

        ans = ''
        #On
        if any([self.result_vector[0][i]==1 for i in range (len(self.result_vector[0]))]) :
            ans = 1
            ##print('A')
        #Off now
        elif any ([self.result_vector[0][i]==0 for i in range (len(self.result_vector[0]))]):
            ans = 0
            #print('B')

        #In future
        elif all ([self.result_vector[0][i]==-1 for i in range (len(self.result_vector[0]))]):
            ans = -1
            #print('C')


        return [ans, [self.result_vector,self.future_on]]
         



#sched_for_button = [[1, "08:44:00", "09:44:00"], [6, "13:45:40", "14:00:00"], [3, "14:31:00", "14:44:00"],[5, "17:29:00", "17:29:10"], [6, "01:47:20", "14:37:20"], [6, "19:00:00", "20:00:00"]]

#sched_for_button =[[3, "17:46:00", "17:46:10"],[3, "17:48:00", "17:48:10"]]
#a = ScheduledEvents(sched_for_button)



class sched_file:
    def __init__(self, master, ip, filename, path,local_ip):
        self.master = master
        self.filename = path + filename + '_' + (ip) + '.csv'
        self.loc_fname = path + filename + '.csv'
        self.ip = ip
        self.local_ip= local_ip
        self.load_csv()


    def save_csv(self, mat, exists=''):  # save sched table to CSV file

        if exists != 'new':
            non_empty_cells = 0
            for v in range(self.master.gui_rows):
                if self.master.row_vars[v][0].get() != "":
                    non_empty_cells += 1
                else:
                    break

            mat = []

            for r in range(non_empty_cells):
                newrow = []
                for c in range(len(self.master.headers) - 1):
                    if c == 0:
                        newrow.append(r)
                    else:
                        newrow.append(self.master.row_vars[r][c].get())
                mat.append(newrow)
            mat.insert(0, self.master.headers)
        else:
            pass

        outputfile = open(self.filename, 'w', newline="")
        outputwriter = csv.writer(outputfile)
        outputwriter.writerows(mat)
        outputfile.close()
        self.master.master.write2log("%s [saved OK]" % self.filename)

        self.reload1(mat)


    def reload1(self, mat):
        self.load_csv()
        self.master.tasks_total = self.tasks_total
        self.master.sch_file = mat
        self.master.continue_task = self.continue_task


    def load_csv(self):

        def read_csv(file_in):
            # check file exist
            if os.path.isfile(file_in) == True:
                with open(file_in, 'r') as f:
                    reader = csv.reader(f)
                    your_list = list(reader)
                    self.sch_file = your_list
            else:
                self.master.master.write2log(self.filename + " [does not exist]")

                mat = []
                mat.append(self.master.headers)
                mat.append(["1", "on", [6], "23:07:00", "01:08:00", "1"])
                self.tasks_total = 1
                self.save_csv(mat, 'new')
                read_csv(self.filename)

        if self.ip == self.local_ip:
            subprocess.run('cp %s %s'%(self.loc_fname,self.filename),shell=True)

        read_csv(self.filename)
        self.tasks_total = (len(self.sch_file)) - 1
        self.continue_task = ['on' for y in range(self.tasks_total)]
        self.master.master.write2log("%s [loaded OK]" % self.filename)


