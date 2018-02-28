import gpiozero
from signal import pause
import threading
# import use_lcd

class LocSwitch:
    def __init__(self,button_pin=20,relay_pin=4, name='No-Name'):
        self.button, self.relay= None, None
        self.button_pin = button_pin
        self.relay_pin = relay_pin
        valid_gpios = [4,17,27,22,5,6,13,19,26,20,21,16,12,25,23,24,18]
        self.press_counter = 0
        self.name=name

        if self.button_pin in valid_gpios \
                    and self.relay_pin in valid_gpios \
                    and self.button_pin != self.relay_pin:
            self.t = threading.Thread(name='thread_gpio_'+str(self.relay_pin), target=self.init_gpio)
            self.t.start()
        else:
            print('pin definition error')
                
    def init_gpio(self):
        try:
            self.button=gpiozero.Button(self.button_pin)
            self.relay=gpiozero.OutputDevice(self.relay_pin)
            self.relay.source = self.button.values
            self.button.when_pressed = self.notify
            print('gpio init successfully')
        except:
            print("init gpio fail")

        pause()


    def notify(self):
        self.press_counter += 1
        print('Switch', self.name, 'pressed', self.press_counter, 'times', self.t.name)

    @property
    def get_status(self):
        return [self.button.value, self.relay.value]


             
if __name__== "__main__":
    a=LocSwitch(20,4)
