import lcddriver
import time

class MyLCD():
    def __init__(self):
        self.display=lcddriver.lcd()
        self.clear_lcd()
        self.boot_test()

    def boot_test(self):
        r=16
        for i in range(int(r/2)):
            text1, text2=' '*r, ' '*r
            self.left_str(text_in1=str(text1) ,to=0.5)

    def clear_lcd(self):
        self.display.lcd_clear()
        
    def center_str(self, text_in1='', text_in2='',to=1):
        text_out1=" "*round((16-len(text_in1))/2)+text_in1
        text_out2=" "*round((16-len(text_in2))/2)+text_in2
        self.display_on_lcd(text1=text_out1, text2=text_out2, to=to)

    def left_str(self, text_in1='', text_in2='', to=1):
        self.display_on_lcd(text1=text_in1, text2=text_in2, to=to)

    def display_on_lcd(self, text1='', text2='', to=1):
        self.display.lcd_display_string(text1, 1)
        self.display.lcd_display_string(text2, 2)
        time.sleep(to)
        self.clear_lcd()
        


if __name__=="__main__":
    lcd=MyLCD()
