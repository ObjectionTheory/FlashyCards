from dothat import backlight, lcd, touch
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

backlight.sweep(0.5)
