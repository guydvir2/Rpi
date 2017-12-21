import csv
from sys import platform
import os.path
import datetime


class sched_file:
    def __init__(self,filename='schedule',path=''):
        #self.master = master
        if path =='':
            path= self.platf()
        self.filename =path+ filename+'_'+'.csv'
        self.load_csv()
        #print(self.filename)

    def platf (self):
        if platform == 'linux':
            path = "/home/guy/PythonProjects/"
        elif platform == 'darwin':
            path = "~/PythonProjects/"
        elif platform == 'win32':
            path = "d:\\PythonProjects\\"
        return path
    
    def save_csv(self,mat): # save sched table to CSV file
##        mat=[]
##        try:
##            mat.append(master.headers)
##        except:
##            print("NOT FOUND")
##            NameError
##            mat.append(["Task#","On/off","Days","Start","End","Switch","Next On/Off"])
##        mat.append(self.sch_file)

##        non_empty_cells=0
##        for v in range(self.tasks_total):
##            if self.row_vars[v][0].get() !="" :#or sched_entries.status[v][0].get() !='None' :
##                non_empty_cells +=1
##            else:
##                break
##
##        for r in range(non_empty_cells):
##            newrow=[]
##            for c in range(len(self.headers)-1):
##                if c==0:
##                    newrow.append(r)
##                else:
##                    #print("r=",r,"c=",c, self.row_vars[r][c].get())
##                    newrow.append(self.row_vars[r][c].get())
##            mat.append(newrow)
            
        outputfile=open(self.filename,'w',newline="")
        outputwriter = csv.writer(outputfile)
        outputwriter.writerows(mat)
        outputfile.close()
        print("[%s] %s saved OK"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        self.filename))
        
    def update_database(self):
        #self.load_csv()
        #self.loop.sch_file=self.sch_file
        pass

    def load_csv(self):

        def read_csv(file_in):
            if os.path.isfile(file_in) == True:                         #Check if file exists
                with open(file_in, 'r') as f:
                    reader = csv.reader(f)
                    your_list = list(reader)
                    self.sch_file=your_list
            else:
                print("NOT EXISTS!!")
                mat=[]
                try:
                    mat.append(master.headers)
                except:
                    NameError
                    mat.append(["Task#","On/off","Days","Start","End","Switch","Next On/Off"])
                    
                mat.append(["1","on",[6],"23:07:00","01:08:00","1"])
                self.save_csv(mat)
                read_csv(self.filename)
                
        read_csv(self.filename)
        self.tasks_total=(len(self.sch_file))-1
        self.continue_task= ['on' for y in range(self.tasks_total)]
        #self.master.master.write2log("[%s] %s loaded OK"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.filename))
        print("[%s] %s loaded OK"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        self.filename))

    def print_csv(self):
        print(self.sch_file)
        print("Total tasks:%d"%self.tasks_total)


