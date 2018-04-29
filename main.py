from dothat import backlight, lcd, touch
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

i = 0
while True:
    backlight.sweep(i)
    i += 0.001
