import gpiozero
from signal import pause
import threading
from time import sleep
import datetime


class LocSwitch:
    def __init__(self, button_pin=20, relay_pin=4, name='No-Name', mode='toggle'):
        self.button, self.relay = None, None
        self.button_pin = button_pin
        self.relay_pin = relay_pin
        self.valid_gpios = [4, 17, 27, 22, 5, 6, 13, 19, 26, 20, 21, 16, 12, 25, 23, 24, 18, 7]
        self.press_counter = 0
        self.name, self.mode = name, mode
        self.last_state, self.current_state = None, None
        self.logbook = []

        self.validate_before_run()

    def validate_before_run(self):
        if self.mode in ['toggle', 'press']:
            if self.button_pin in self.valid_gpios \
                    and self.relay_pin in self.valid_gpios \
                    and self.button_pin != self.relay_pin:
                self.t = threading.Thread(name='thread_gpio_' + str(self.relay_pin), target=self.init_gpio)
                self.t.start()
                self.log_record('init in [%s] mode on [%s] ' % (self.mode, self.t.name))
            else:
                self.log_record('pin definition error')
        else:
            self.log_record('err- modes can be "toggle" or "press" only')

    def init_gpio(self):
        try:
            self.button = gpiozero.Button(self.button_pin)
            self.relay = gpiozero.OutputDevice(self.relay_pin)
            if self.mode == 'toggle':
                self.button.when_pressed = self.toggle_switch
            elif self.mode == 'press':
                self.relay.source = self.button.values
                self.button.when_pressed = self.press_switch
                self.button.when_released = self.release_switch
            self.log_record('gpio init successfully')
            pause()

        except:
            self.log_record("init gpio fail, Code quit")
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
        if value in [0, 1]:
            add = 'code'
            if self.mode == 'press':
                self.press_switch(add)
            elif self.mode == 'toggle':
                self.toggle_switch(add)
        else:
            msg = '[%s] must be [0,1]' % (self.name)
            self.log_record(msg)
        return msg

    def log_record(self, text1=''):
        msg = ''
        time = str(datetime.datetime.now())[:-5]
        msg = '[%s]: [%s] %s' % (time, self.name, text1)
        self.logbook.append(msg)
        print(self.logbook[-1])

    def watch_dog(self):
        def run_watchdog():
            last_state = 0
            while True:
                if self.relay.value != last_state:
                    self.log_record("[watch_dog] [GPIO %s] [%s]" % (self.relay_pin, self.switch_state[0]))
                last_state = self.relay.value
                sleep(1)

        self.t2 = threading.Thread(name='thread_watchdog', target=run_watchdog)
        self.t2.start()


if __name__ == "__main__":
    a = LocSwitch(21, 4, mode='toggle', name="GUYDVIR")
    sleep(2)
    a.watch_dog()
    a.switch_state = 1
    sleep(2)
    a.switch_state = 0
    c = LocSwitch(20, 4, mode='press', name="GUYDVIR2")
