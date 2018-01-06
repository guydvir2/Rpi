import tkinter as tk
import gpiozero
from time import sleep
from gpiozero import OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory


class UpDownButton(tk.Frame):

    
    class HWRemoteOutput:
    #This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
        def __init__(self, master, ip, output_pins):
            self.master = master
            factory = PiGPIOFactory(host=ip)
            self.output_pins= ["Pin_"+str(output_pins[i]) for i in range(len(output_pins))]
            for sw in range(len(self.output_pins)):
                self.output_pins[sw] = OutputDevice(output_pins[sw], pin_factory=factory,initial_value=False)
                
            print("RemoteOutput Init %s, IP:%s, GPIO pins:%s"%(self.master.nick, ip, output_pins))


        #Make the switch
        def set_state(self, sw, state):
            if state == 1:
                self.output_pins[sw].on()
            elif state == 0:
                self.output_pins[sw].off()

        #Inquiry
        def get_state(self):
            stat=[]
            for sw in range(len(self.output_pins)):
                stat.append(self.output_pins[sw].value)
            return stat

    
    class Indicators:
        def __init__(self,master, frame ):
            self.master = master
            self.frame = frame
            self.t = 2
            self.indicators = ['indicator'+str(i) for i in range(self.t)]
            self.build_gui()
            self.update_indicators()
            
            
        def update_indicators(self):
            for i in range(self.t):
                if self.master.get_state()[i] == False:
                    self.indicators[i].config(bg="red")
                elif self.master.get_state()[i] == True:
                    self.indicators[i].config(bg="green")
                    
            root.after(500, self.update_indicators)

        def build_gui(self):
            ofset=8
            for i in range(self.t):
                self.indicators[i] = tk.Label(self.frame, width=1, height=1, text="", bg='blue',relief=tk.SUNKEN)
                self.indicators[i].grid(row=i, column=0, sticky=tk.NE,pady=ofset, padx=ofset)


    class HWRemoteInput:
        #This class create a link between input_pins(HW buttons) to output pins
        def __init__(self, master, ip, input_pins):
            self.master = master
            factory = PiGPIOFactory(host=ip)
            
            self.input_pins= ["Pin_"+str(input_pins[i]) for i in range(len(input_pins))]
            for sw in range(len(self.input_pins)):
                self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
                self.input_pins[sw].when_pressed = lambda arg=sw :self.pressed(arg)

            print("RemoteInput Init-%s, IP:%s, GPIO pins:%s"%(self.master.nick,ip, input_pins))


        #Detect press and make switch
        def pressed(self,i):
            self.master.switch_type = 'HWButton, '
            self.master.external_command(i, [1,0][self.master.HW_output.get_state()[i]])


        def get_state(self):
            stat=[]
            for sw in range(len(self.input_pins)):
                stat.append([self.input_pins[sw].value])
            return stat


    def __init__(self, master, nickname='', text_up='UP', text_down='DOWN', width=15, height=3, hw_in=[], hw_out=[], ip_in='', ip_out=''):
        
        tk.Frame.__init__(self, master)
        self.nick = nickname
        self.master = master
        self.text_up = text_up
        self.text_down = text_down
        self.but_stat = []

        if hw_out == '':
            hw_out = hw_in
        elif hw_in == '':
            hw_in = hw_out

        if ip_in == '':
            ip_in = ip_out
        elif ip_out =='':
            ip_out = ip_in
        
        self.build_buttons(text_up, text_down, width, height)
        
        self.HW_output = self.HWRemoteOutput(self, ip_out, hw_out)
        self.Indicators(self.HW_output, self)
        self.HW_input = self.HWRemoteInput(self, ip_in, hw_in)

        self.switch_type=''


    def build_buttons(self, text_up, text_down, width, height):

        but1_var = tk.IntVar()
        but1 = tk.Checkbutton(self, text=text_up, width=width, height=height, indicatoron=0, variable=but1_var,command=self.com_up)
        but1.grid(row=0, column=0, pady=5)

        but2_var = tk.IntVar()
        but2 = tk.Checkbutton(self, text=text_down, width=width, height=height, indicatoron=0, variable=but2_var,command=self.com_down)
        but2.grid(row=1, column=0)

        label = tk.Label(self, text=self.nick)
        label.grid(row=2, column=0)

        self.but_stat = [but1_var, but2_var]



    def com_up(self, nick=''):
        if nick == '':
            self.switch_type = 'SFButton, '

        if self.but_stat[0].get() == 1:
            if self.but_stat[1].get() == 1:
                self.but_stat[1].set(0)
                self.exec_switch(0, self.but_stat[1].get())
                #self.switch_type = self.switch_type+self.text_up+', Off'
                sleep(1)
                self.exec_switch(self.but_stat[0].get(), self.but_stat[1].get())
                #self.switch_type = self.switch_type+self.text_up+', On'
            elif self.but_stat[1].get() == 0:
                self.exec_switch(self.but_stat[0].get(), self.but_stat[1].get())
        elif self.but_stat[0].get() == 0:
            self.exec_switch(self.but_stat[0].get(), self.but_stat[1].get())



    def com_down(self, nick=''):
        if nick == '':
            self.switch_type = 'SFButton, '
            
        if self.but_stat[1].get() == 1:
            if self.but_stat[0].get() == 1:
                self.but_stat[0].set(0)
                self.exec_switch(self.but_stat[0].get(), 0)
                sleep(1)
                self.exec_switch(self.but_stat[0].get(), self.but_stat[1].get())
            elif self.but_stat[0].get() == 0:
                self.exec_switch(self.but_stat[0].get(), self.but_stat[1].get())
        elif self.but_stat[1].get() == 0:
            self.exec_switch(self.but_stat[0].get(), self.but_stat[1].get())



    def external_command(self, sw, state):
        
        self.but_stat[sw].set(state)
                
        if sw == 0:
            self.com_up(nick = self.switch_type)
        elif sw == 1:
            self.com_down(nick = self.switch_type)



    def exec_switch(self, up_stat, down_stat):

        self.HW_output.set_state(0,up_stat)
        self.HW_output.set_state(1, down_stat)

        print([self.nick, self.switch_type, self.HW_output.get_state()])



    def get_state(self):
        return self.HW_output.get_state()




class ToggleButton(tk.Frame):

    
    class HWRemoteOutput:
    #This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
        def __init__(self,master, ip, output_pins):
            factory = PiGPIOFactory(host=ip)
            self.master = master
            self.output_pins= ["Pin_"+str(output_pins[i]) for i in range(len(output_pins))]
            for sw in range(len(self.output_pins)):
                self.output_pins[sw] = OutputDevice(output_pins[sw], pin_factory=factory,initial_value=False)
                
            print("RemoteOutput Init %s, IP:%s, GPIO pins:%s"%(self.master.nick, ip, output_pins))


        #Make the switch
        def set_state(self, sw, state):
            if state == 1:
                self.output_pins[sw].on()
            elif state == 0:
                self.output_pins[sw].off()

        #Inquiry
        def get_state(self):
            stat=[]
            for sw in range(len(self.output_pins)):
                stat.append(self.output_pins[sw].value)
            return stat

    
    class Indicators:
        
        def __init__(self,master, frame ):
            self.master = master
            self.frame = frame
            self.t = 1
            self.indicators = ['indicator'+str(i) for i in range(self.t)]
            self.build_gui()
            self.update_indicators()
            
            
        def update_indicators(self):
            for i in range(self.t):
                if str(self.master.get_state()[i]) == "False":
                    self.indicators[i].config(bg="red")
                elif str(self.master.get_state()[i]) == "True":
                    self.indicators[i].config(bg="green")
            root.after(500, self.update_indicators)


        def build_gui(self):
            ofset=8
            for i in range(self.t):
                self.indicators[i] = tk.Label(self.frame, width=1, height=1, text="", bg='blue',relief=tk.SUNKEN)
                self.indicators[i].grid(row=i, column=0, sticky=tk.NE, pady=ofset, padx=ofset)


    class HWRemoteInput:
        #This class create a link between input_pins(HW buttons) to output pins
        def __init__(self, master, ip, input_pins):
            self.master = master
            factory = PiGPIOFactory(host=ip)
            
            self.input_pins= ["Pin_"+str(input_pins[i]) for i in range(len(input_pins))]
            for sw in range(len(self.input_pins)):
                self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
                self.input_pins[sw].when_pressed = lambda arg=sw :self.pressed(arg)

            print("RemoteInput Init-%s, IP:%s, GPIO pins:%s"%(self.master.nick,ip, input_pins))

        #Detect press and make switch
        def pressed(self,i):
            
            self.master.switch_type = 'HWButton Switch'
            self.master.external_command(i,[1,0][self.master.HW_output.get_state()[i]])

        def get_state(self):
            stat=[]
            for sw in range(len(self.input_pins)):
                stat.append([self.input_pins[sw].value])
            return stat

    
    def __init__(self, master, nickname='Button', height=3, width=15, ip_in='', input_pins=[], ip_out='', output_pins=[]):
        
        tk.Frame.__init__(self, master)
        
        if ip_in == '':
            ip_in = ip_out
        self.nick = nickname
        self.master = master
        self.HW_output = self.HWRemoteOutput(self, ip_out, output_pins)
        self.HW_input = self.HWRemoteInput(self, ip_in, input_pins)
        self.build_gui(self, nickname, height, width)
        self.switch_type=''
        
        


    def build_gui(self, master, nickname, height, width):
        
        self.but_vat = tk.IntVar()
        button = tk.Checkbutton(self, text = nickname, variable=self.but_vat, indicatoron=0, height=height, width= width, command=self.SFbutton_pressed)
        button.grid(row=0, column=0, padx=3)

        self.txtvar = tk.IntVar()
        self.txtvar.set(0)
        timeout_entry = tk.Entry(self, textvariable=self.txtvar, width=3, bg="white", fg='black', justify=tk.CENTER)
        timeout_entry.grid(row=1, column=0, sticky=tk.E, padx=6)

        timeout_label = tk.Label(self, text='TimeOut [min]')
        timeout_label.grid(row=1, column=0, sticky= tk.W, padx=6 , pady=3)
        self.Indicators(self.HW_output, self)


    def execute_command(self,state,txt=''):
    
        self.but_vat.set(state)
        self.HW_output.set_state(0,state)

        print([self.nick, self.switch_type, state, txt])


    def external_command(self,i,state):
        #i irrelvant 
        self.execute_command(state)


    def SFbutton_pressed(self):
    
        self.switch_type = 'SFButton'
        if self.but_vat.get() == 1 and self.txtvar.get() >0:
                self.execute_command(1, 'AutoOff %d minutes'%self.txtvar.get())
                self.after(self.txtvar.get()*1000, self.execute_command, 0)
                self.txtvar.set(0)

        else:
            self.execute_command(self.but_vat.get())


    def get_state(self):
        return self.HW_output.get_state()


root = tk.Tk()
but1 = UpDownButton(root, "Room_Window",'UP','DOWN',10,3,[21,3],[4,17],'192.168.2.113','192.168.2.113')
but1.grid()

#but2 = ToggleButton(root,"Water Heater", height=3, width=15, ip_out='192.168.2.113', output_pins=[4], ip_in='192.168.2.113', input_pins=[21])
#but2.grid(row=1, column=0)

#but3 = ToggleButton(root, "GUY DVIR", height=3, width=15, ip_out='192.168.2.113', output_pins=[5], ip_in='192.168.2.113', input_pins=[22])
#but3.grid(row=1, column=1)

root.mainloop()
