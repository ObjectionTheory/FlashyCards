from dothat import backlight, lcd, touch
import RPi.GPIO as GPIO

import line
import json

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

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