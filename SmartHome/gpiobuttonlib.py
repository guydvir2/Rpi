""" This Lib is used with ButtonLib2 as HW module designed by me"""
from gpiozero.pins.pigpio import PiGPIOFactory
import gpiozero
import pigpio
from gpiozero import OutputDevice
import datetime
import os


class Com2Log:
    """ This class sends status logs to main GUI"""

    def __init__(self, master, nick):
        self.nick = nick
        self.master = master

    def message(self, text1):

        time_now = str(datetime.datetime.now())[:-5]
        text2 = '[%s] %s' % (time_now, text1)
        try:
            self.master.master.master.master.master.master.master.write2log(text2)
        except AttributeError:
            print(text2)


class Indicators:
    """ This Calss displays output state of GPIO """

    def __init__(self, master, frame, pdy=0, pdx=3, cols=[]):
        self.master = master
        self.frame = frame
        self.x = 0
        self.update_indicators()
        self.run_id = None

    def update_indicators(self):

        if self.x == 120 or self.x == 1:
            self.ping_it()
            self.x = 1
        elif self.x > 20:
            self.master.master.conn_lbl['style'] = 'B.TLabel'

        self.x += 1

        for i, but in enumerate(self.master.master.buts):
            if self.master.get_state()[i] == False:
                fg, text2 = 'red', ' (Off)'
            elif self.master.get_state()[i] == True:
                fg, text2 = 'green', ' (On)'

            but.config(fg=fg)
            but.config(text=self.master.master.buts_names[i] + text2)

        self.run_id = self.frame.after(500, self.update_indicators)

    def ping_it(self):
        conn_stat = ['Connected', 'Lost']
        style = ['Green.TLabel', 'Red.TLabel']
        ping_result = os.system('ping %s -c 1 >NULL' % self.master.master.ip_out)
        self.master.master.conn_status_var.set(conn_stat[ping_result])
        self.master.master.conn_lbl['style'] = style[ping_result]

    def close_device(self):
        if self.run_id != None:
            self.master.master.conn_status_var.set('Stop')
            self.frame.after_cancel(self.run_id)
            self.x = 0


class HWRemoteInput:
    # This class create a link between input_pins(HW buttons) to output pins
    def __init__(self, master=None, ip='', input_pins=[]):
        self.master = master
        self.factory = PiGPIOFactory(host=ip)
        self.input_pins = []

        if self.master is None:
            nick = 'RemoteInput Device'
        else:
            nick = self.master.nick

        self.com = Com2Log(self.master, nick)
        self.hardware_config(input_pins=input_pins, ip=ip)

    def hardware_config(self, input_pins,ip):
        for sw, pin in enumerate(input_pins):
            self.input_pins.append(gpiozero.Button(pin, pin_factory=self.factory))
            self.input_pins[sw].when_pressed = lambda arg=[sw, 1]: self.pressed(arg)
            # Line below is used when button switched off - setting the command to off
            self.input_pins[sw].when_released = lambda arg=[sw, 0]: self.pressed(arg)

        self.com.message("[Remote-Intput][IP:%s][GPIO pins:%s]" % (ip, input_pins))

    # Detect press and make switch
    def pressed(self, arg):
        self.master.switch_type = 'HWButton Switch'
        sw, state = arg[0], arg[1]  #
        self.master.ext_press(sw, state, self.master.switch_type)

    def get_state(self):
        stat = []
        for sw in (self.input_pins):
            stat.append([sw.value])
        return stat

    # Close device
    def close_device(self):
        for sw in self.output_pins:
            sw.close()
        self.com.message("[Device shut done]")


class HWRemoteOutput:
    # This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
    def __init__(self, master=None, ip='', output_pins=[]):
        self.master = master
        self.factory = PiGPIOFactory(host=ip)
        self.output_pins = []

        if self.master is None:
            nick = 'RemoteOutput Device'
        else:
            nick = self.master.nick

        self.com = Com2Log(self.master, nick)
        self.hardware_config(output_pins=output_pins,ip=ip)

    def hardware_config(self, output_pins,ip):
        for sw, pin in enumerate(output_pins):
            self.output_pins.append(OutputDevice(pin, pin_factory=self.factory, initial_value=False))

        self.com.message("[Remote-Output][IP:%s][GPIO pins:%s]" % (ip, output_pins))

    # Make the switch
    def set_state(self, sw, state):
        if state == 1:
            self.output_pins[sw].on()
        elif state == 0:
            self.output_pins[sw].off()

    def get_state(self):
        stat = []
        for pin in self.output_pins:
            stat.append(pin.value)
        return stat

    def close_device(self):
        for sw in self.output_pins:
            sw.close()
        self.output_pins[0].close()
        self.com.message("[Device shut done]")
        
        
if __name__ == "__main__":
    a= HWRemoteOutput(ip='192.168.2.113', output_pins=[11])
    a.set_state(0,1)
    print(a.get_state())
    a.close_device()

    b = HWRemoteInput(ip='192.168.2.113', input_pins=[12])
