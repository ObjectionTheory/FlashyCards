import dothat as hat
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

hat.lcd.write("Hello World!")
