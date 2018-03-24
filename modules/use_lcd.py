import lcddriver
import time

class MyLCD():
    def __init__(self):
        self.display=lcddriver.lcd()
        self.clear_lcd()
        #self.boot_test()

    def boot_test(self):
        TO=0.5
        self.left_str(text1='left_up' ,text2='left_down',to=TO)
        self.right_str(text1='right_up',text2='right_down' ,to=TO)
        self.center_str(text1='center_up',text2='center_down',to=TO)

    def clear_lcd(self):
        self.display.lcd_clear()
        
    def center_str(self, text1='', text2='',to=0):
        text_out1=" "*round((16-len(text1))/2)+text1
        text_out2=" "*round((16-len(text2))/2)+text2
        self.display_on_lcd(text1=text_out1, text2=text_out2, to=to)

    def left_str(self, text1='', text2='', to=0):
        self.display_on_lcd(text1=text1, text2=text2, to=to)
        
    def right_str(self, text1='', text2='', to=0):
        text_out1=' '*(16-len(text1))+text1
        text_out2=" "*(16-len(text2))+text2
        self.display_on_lcd(text1=text_out1, text2=text_out2, to=to)

    

    def display_on_lcd(self, text1='', text2='', to=0):
        self.display.lcd_display_string(text1, 1)
        self.display.lcd_display_string(text2, 2)
        time.sleep(to)
        if to != 0:
        	self.clear_lcd()
        

if __name__=="__main__":
    lcd=MyLCD()
