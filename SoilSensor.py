import RPi.GPIO as GPIO
import time

#Name:Yekai
#Date:2026/4/20

# GPIO SETUP
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("Water Detected!")
    else:
        print("Water Detected!")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # detect the pin goes high or low 
GPIO.add_event_callback(channel, callback)  # set call back function

while True:
    time.sleep(1)
