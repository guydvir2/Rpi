import lcddriver
import time

class MyLCD():
    def __init__(self):
        self.display=lcddriver.lcd()
        self.clear_lcd()
        self.boot_test()

    def boot_test(self):
        r=16
        for i in range(int(r)):
            text1, text2='-'*i, '-'*i
            self.left_str(text1=str(text1) ,text2=str(text2), to=0.1)

    def clear_lcd(self):
        self.display.lcd_clear()
        
    def center_str(self, text1='', text2='',to=0):
        text_out1=" "*round((16-len(text1))/2)+text1
        text_out2=" "*round((16-len(text2))/2)+text2
        self.display_on_lcd(text1=text_out1, text2=text_out2, to=to)

    def left_str(self, text1='', text2='', to=0):
        self.display_on_lcd(text1=text1, text2=text2, to=to)

    def display_on_lcd(self, text1='', text2='', to=0):
        self.display.lcd_display_string(text1, 1)
        self.display.lcd_display_string(text2, 2)
        time.sleep(to)
        if to != 0:
        	self.clear_lcd()
        

if __name__=="__main__":
    lcd=MyLCD()
