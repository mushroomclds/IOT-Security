import time
import RPi.GPIO as GPIO
from pygame import mixer
'''from subprocess import call
call(["aplay", "jazz.wav"])
import time
time.sleep(5)'''

# Initialize pygame mixer
mixer.init()

# Remember the current and previous button states
current_state = True
prev_state = True

# Load the sounds
sound = mixer.Sound('jazz.wav')


try:
    while True:
        current_state = False #make this get value from sensor 
        if (current_state == False) and (prev_state == True):
            sound.play()
        prev_state = current_state

# When you press ctrl+c, this will be called
finally:
    GPIO.cleanup()
