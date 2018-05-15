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
        """Relay refers to HW that makes the switch AKA "OUTPUT". Button refer to buttons physical HW AKA "INPUT" """
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
            self.log_record('init [%s mode][GPIO in/out:%s/%s] ' % (self.mode, self.button_pin, self.relay_pin))
        else:
            self.log_record('err- modes can be "toggle" or "press" only')

    def start_gpio_hw(self):
        try:
            self.button = gpiozero.Button(self.button_pin)
            self.relay = gpiozero.OutputDevice(self.relay_pin)

            if self.mode == 'toggle':
                pass
                self.button.when_pressed = self.toggle_switch
            elif self.mode == 'press':
                #self.relay.source = self.button.values
                self.button.when_pressed = self.press_switch
                self.button.when_released = self.release_switch
            self.log_record('GPIO initialize successfully')
            pause()

        except NameError:
            self.log_record("GPIO initialize fail.\nquit")
            quit()

    def press_switch(self, add=''):
        """ Press state only"""

        # Case of DoubleSwitch
        self.off_other_switch()
        #
        
        self.relay.on()
        if add == '':
            add = 'button'
        self.press_counter += 1
        msg = ('[pressed] [%s] [%d times]' % (add, self.press_counter))
        self.log_record(msg)

    def release_switch(self, add=''):
        """ Press state only"""
        
        # Case of DoubleSwitch
        self.off_other_switch()
        #
        
        self.relay.off()
        if add == '':
            add = 'button'
        msg = ('[released] [%s]' % (add))
        self.log_record(msg)

    def toggle_switch(self, pressed_by='', state=None):
        """ Toggle State only"""
        text=pressed_by
        self.last_state = self.relay.value
        # in case of DoubleSwitch
        self.off_other_switch()
        #
        if pressed_by == '':
            self.relay.toggle()
        elif pressed_by == 'code':
            if state == 0:
                self.relay.off()
            elif state == 1:
                self.relay.on()
                
        self.current_state = self.relay.value
        self.press_counter += 1
        msg = ('[%s --> %s] pressed [%s] [%d] times' % (self.last_state,
                                                        self.current_state, text, self.press_counter))
        self.log_record(msg)

    @property
    def switch_state(self):
        return [self.relay.value, self.button.value]

    """ Using for code change state- allways as toggle"""
    @switch_state.setter
    def switch_state(self, value):

        if value == 0:
            if self.relay.value is True:
                self.toggle_switch(pressed_by='code', state=value)
                #self.off_other_switch()
                #self.relay.off()
        elif value == 1:
            if self.relay.value is False:
                self.toggle_switch(pressed_by='code', state=value)
                #self.off_other_switch()
                #self.relay.on()
        else:
            msg = '[%s] must be [0,1]' % self.name
            self.log_record(msg)

    # @switch_state.setter
    # def switch_state(self, value):
    #     if value == 0:
    #         if self.mode == 'toggle':
    #             if self.relay.value is True:
    #                 self.toggle_switch(add='code')
    #         elif self.mode == "press":
    #             if self.relay.value is True:
    #                 self.release_switch(add='code')
    #                 self.relay.off()
    #     elif value == 1:
    #         if self.mode == 'toggle':
    #             if self.relay.value is False:
    #                 self.toggle_switch(add='code')
    #         elif self.mode == "press":
    #             if self.relay.value is False:
    #                 self.press_switch(add='code')
    #                 self.relay.on()
    #     else:
    #         msg = '[%s] must be [0,1]' % self.name
    #         self.log_record(msg)

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
            last_state = self.relay.value
            while True:
                if self.relay.value != last_state:
                    self.log_record("[WatchDog] [GPIO %s] [%s]" % (self.relay_pin, self.switch_state[0]))
                    last_state = self.relay.value
                sleep(0.1)

        sleep(1)
        self.t2 = threading.Thread(name='thread_watchdog', target=run_watchdog)
        self.t2.start()
        self.log_record('[WatchDog] init')


class DoubleSwitch:
    def __init__(self, button_pin1, button_pin2, relay_pin1, relay_pin2, mode='press', name='Double_switch',
                 sw0_name='/SW#0',
                 sw1_name='/SW#1', ext_log=None):
        self.switch0 = SingleSwitch(button_pin=button_pin1, relay_pin=relay_pin1, mode=mode, name=name + sw0_name,
                                    ext_log=ext_log)
        self.switch1 = SingleSwitch(button_pin=button_pin2, relay_pin=relay_pin2, mode=mode, name=name + sw1_name,
                                    ext_log=ext_log)
        self.switch0.add_other_switch(self.switch1)
        self.switch1.add_other_switch(self.switch0)

    def watch_dog(self):
        self.switch0.watch_dog()
        self.switch1.watch_dog()


if __name__ == "__main__":
    if ok_module is True:
        #### CASE A- SingleSwitch ########

        a = SingleSwitch(26, 20, mode='press', name="LocalSwitch_SW#1")
        # a pause due to use of thread
        sleep(1)
        a.watch_dog()
        sleep(1)
        a.switch_state = 1
        sleep(2)
        a.switch_state = 0
        sleep(0.11)

        a.switch_state = 1

        b = SingleSwitch(19, 21, mode='toggle', name="LocalSwitch_SW#2")
        sleep(1)
        b.switch_state = 1
        sleep(2)
        b.switch_state = 0
    else:
        print("Can't run without gpiozero module")

        #### CASE B - Using Double Switch#########
        # doubleswitch = DoubleSwitch(26, 19, 21, 20, name='Room#1_Shades')
