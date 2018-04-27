import subprocess
from sys import platform


class WifiControl:
    def __init__(self):
        self.plat = platform
        print('booted on %s system' % self.plat)
        self.on_command = 'nmcli radio wifi on'.split()
        self.off_command = 'nmcli radio wifi off'.split()
        self.pwd = None

    def read_pwd_fromfile(self):
        filename='/home/guy/Documents/github/Rpi/modules/p.txt'
        with open(filename,'r')as f:
            self.pwd=f.read()

    def get_status(self):
        a1 = subprocess.Popen(['nmcli', 'radio', 'all'], stdout=subprocess.PIPE)
        tup_output = a1.communicate()
        print(tup_output)

    def shut_wifi(self):
        a1 = subprocess.Popen(['sudo', '-S'] + self.off_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True)
        tup_output = a1.communicate(self.pwd + '\n')[1]
        self.get_status()



a = WifiControl()
a.read_pwd_fromfile()
# a.shut_wifi()
# a.get_status()

