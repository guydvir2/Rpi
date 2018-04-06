from signal import pause
import threading
from time import sleep
import datetime

try:
    import gpiozero

    ok_module = True
except ImportError:  # ModuleNotFoundError:
    print("Fail to obtain gpiozero module")
    ok_module = False


class SingleSwitch:
    def __init__(self, button_pin=20, relay_pin=4, name='No-Name', mode='press', ext_log=None):
        self.button, self.relay = None, None
        self.button_pin = button_pin
        self.relay_pin = relay_pin
        self.valid_gpios = [4, 17, 27, 22, 5, 6, 13, 19, 26, 20, 21, 16, 12, 25, 23, 24, 18, 7]
        self.press_counter = 0
        self.name, self.mode = name, mode
        self.last_state, self.current_state = None, None
        self.logbook, self.ext_log = [], ext_log
        # case of using Single Switch in DoubleSwitch only
        self.other_SingleSwitch = None

        self.startup()

    def verify_gpio_selection(self):
        if self.button_pin in self.valid_gpios and self.relay_pin in self.valid_gpios and \
                self.button_pin != self.relay_pin:                    
            return 1
        else:
            self.log_record('pin definition error')
            return 0

    def startup(self):
        if self.mode in ['toggle', 'press'] and self.verify_gpio_selection() == 1:
            self.t = threading.Thread(name='thread_gpio_' + str(self.relay_pin), target=self.start_gpio_hw)
            self.t.start()
            self.log_record('init in [%s] mode on [%s] ' % (self.mode, self.t.name))
        else:
            self.log_record('err- modes can be "toggle" or "press" only')

    def start_gpio_hw(self):
        try:
            self.button = gpiozero.Button(self.button_pin)
            self.relay = gpiozero.OutputDevice(self.relay_pin)
            if self.mode == 'toggle':
                self.button = self.toggle_switch
            elif self.mode == 'press':
                self.relay.source = self.button.values
                self.button.when_pressed = self.press_switch
                self.button.when_released = self.release_switch
            self.log_record('GPIO initialize successfully')
            pause()

        except NameError:
            self.log_record("GPIO initialize fail.\nquit")
            quit()

    def press_switch(self, add=''):
        if add == '':
            add = 'button'
        self.press_counter += 1
        msg = ('pressed [%s] [%d] times' % (add, self.press_counter))
        self.log_record(msg)

    def release_switch(self):
        msg = ('[%s] released' % (self.name))
        self.log_record(msg)

    def toggle_switch(self, add=''):
        if add == '':
            add = 'button'
        self.last_state = self.relay.value
        # in case of DoubleSwitch
        self.off_other_switch()
        #
        self.relay.toggle()
        self.current_state = self.relay.value
        self.press_counter += 1
        msg = ('[%s --> %s] pressed [%s] [%d] times' % (self.last_state,
                                                        self.current_state, add, self.press_counter))
        self.log_record(msg)

    @property
    def switch_state(self):
        return [self.relay.value, self.button.value]

    @switch_state.setter
    def switch_state(self, value):
        if value == 0:
            if self.mode == 'toggle':
                if self.relay.value == True:
                    self.toggle_switch()
            elif self.mode == "press":
                if self.relay.value == True:
                    self.release_switch()
                    self.relay.off()
                    print("off")
        elif value == 1:
            if self.mode == 'toggle':
                if self.relay.value == False:
                    self.toggle_switch()
            elif self.mode == "press":
                if self.relay.value == False:
                    #self.press_switch()
                    self.relay.on()
                    print("on")
            
                
                    
        #if value in [0, 1]:
            #add = 'code'
            #if self.mode == 'press':
                #self.press_switch(add)
            #elif self.mode == 'toggle':
                #self.toggle_switch(add)
        #else:
            #msg = '[%s] must be [0,1]' % self.name
            #self.log_record(msg)

    def log_record(self, text1=''):
        msg = ''
        time = str(datetime.datetime.now())[:-5]
        msg = '[%s] [%s] %s' % (time, self.name, text1)
        self.logbook.append(msg)
        print(self.logbook[-1])
        if self.ext_log is not None:
            self.ext_log.append_log(msg)
        return msg

    def add_other_switch(self, other_switch):
        self.other_SingleSwitch = other_switch

    def off_other_switch(self):
        if self.other_SingleSwitch is not None:
            if self.other_SingleSwitch.switch_state[0] is True:
                self.other_SingleSwitch.switch_state = 0
                sleep(0.3)

    def watch_dog(self):
        # run inspection in background to check state of gpios
        def run_watchdog():
            last_state = 0
            while True:
                print(self.relay.value)
                if self.relay.value != last_state:
                    self.log_record("[watch_dog] [GPIO %s] [%s]" % (self.relay_pin, self.switch_state[0]))
                last_state = self.relay.value
                sleep(1)

        self.t2 = threading.Thread(name='thread_watchdog', target=run_watchdog)
        self.t2.start()
    def on(self):
        self.relay.on()


class DoubleSwitch:
    def __init__(self, button_pin1, button_pin2, relay_pin1, relay_pin2, name='Double_switch'):
        self.switch0 = SingleSwitch(button_pin=button_pin1, relay_pin=relay_pin1, mode='toggle', name=name + '/SW#0')
        self.switch1 = SingleSwitch(button_pin=button_pin2, relay_pin=relay_pin2, mode='toggle', name=name + '/SW#1')
        self.switch0.add_other_switch(self.switch1)
        self.switch1.add_other_switch(self.switch0)


if __name__ == "__main__":
    if ok_module is True:
        #### CASE A- SingleSwitch ########

        a = SingleSwitch(21, 4, mode='press', name="LocalSwitch_SW#1")
        # a pause due to use of thread
        sleep(1)
        a.watch_dog()
        sleep(1)
        #a.switch_state = 1
        a.on()
        #sleep(2)
        #a.switch_state = 0

        #b = SingleSwitch(20, 5, mode='press', name="LocalSwitch_SW#2")
        #sleep(1)
        #b.switch_state = 1
        #sleep(2)
        #b.switch_state = 0
    else:
        print("Can't run without gpiozero module")

        #### CASE B - Using Double Switch#########
        #doubleswitch = DoubleSwitch(26, 19, 21, 20, name='Room#1_Shades')
