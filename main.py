from dothat import backlight, lcd, touch
import RPi.GPIO as GPIO

import line
import json

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

<<<<<<< HEAD
backlight.rgb(0, 204, 255)

lastSession = {}

menu = Menu(
    structure = {
        'Continue' : loadCards(lastSession),
        #'Load Card Pack' : cardPacks,
        'Get More Cards' : Menu(
            structure = {
                   k:(lambda k: getCards(k)) for k in line.getAddresses()
            },
        ),
        'Save and Exit' : saveAndExit(),
        'Settings' : {
            'Check Server': line.checkServer()
        }
        
    }
)

def loadCards():
    pass

def saveAndExit():
    pass

def getCards():
    cards = line.getCards()

    '''
def getCardMenu(MenuOption):
    def __init__(self):
        self.addresses = line.getAddresses()

        MenuOption.__init__(self)

    def begin(self):
        self.is_setup = False
        self.running = True

    def setup(self, config):
        MenuOption.setup(self, config)
        self.load_options()
    
    def load_options()'''
=======
i = 0
while True:
    backlight.sweep(i)
    i += 0.001
>>>>>>> b0e490be7d042382c86966a133b8910945652aa8
