import gpiozero
from signal import pause
def func():
    print("hi")
button = gpiozero.Button(2)
buzzer = gpiozero.Buzzer(3)

button.when_pressed= buzzer.toggle

pause()
