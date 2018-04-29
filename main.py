import dothat as hat
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

hat.backlight.sweep(0.5)
