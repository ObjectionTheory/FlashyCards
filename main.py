from dot3k.menu import Menu, MenuOption
from dothat import backlight, lcd, touch
import RPi.GPIO as GPIO
import time
import random

import line
import json

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

backlight.hue(0.8)

class CardSession(MenuOption):
    def __init__(self, app, cards, name, cont=False):
        self.app = app
        self.cards = cards
        self.name = name
        self.cont = cont

        self.currentIndex = 0
        self.indices = [i for i in cards]

        self.back = False
        self.lastUpdate = 0
        self.running = False

        MenuOption.__init__(self)

    def begin(self):
        self.running = False
        self.reset()
        
        if not self.cont:
            print("MEEp")
            self.app.setLastSession(self.name)

    def reset(self):
        
        self.running = True
        lcd.clear()      

    def right(self):
        if not self.running:
            return True
        self.reset()
        self.currentIndex += 1
        self.back = False

        if self.currentIndex == len(self.indices):
            self.currentIndex = 0
        return True

    def left(self):
        if not self.running:
            return False
        self.reset()
        self.currentIndex -= 1
        self.back = False

        if self.currentIndex == -1:
            self.currentIndex = len(self.indices)-1
        return True

    def up(self):
        self.app.favoriteCard(
            self.indices[self.currentIndex],
            self.cards[self.indices[self.currentIndex]],
            True
        )

        return True

    def down(self):
        self.app.favoriteCard(
            self.indices[self.currentIndex],
            self.cards[self.indices[self.currentIndex]],
            False
        )

        return True
    
    def select(self):
        self.reset()
        self.back = not self.back

    def redraw(self, menu):
        
        if self.millis() - self.lastUpdate <= 250:
            return
        
        if not self.running:
            return False

        self.lastUpdate = self.millis()

        lcd.set_cursor_position(0, 1)
        if not self.back:
            lcd.write(self.indices[self.currentIndex])    
        else:
            lcd.write(self.cards[self.indices[self.currentIndex]])

class App:
    def __init__(self):

        self.structure = {}

        with open('local.json') as f:
            self.cards = json.load(f)
            self.config = self.cards['CONFIG']

        self.cards = self.formatCards(self.cards)
        for subject in self.cards:
            for topic in self.cards[subject]:
                self.cards[subject][topic] = CardSession(self, self.cards[subject][topic], subject+"."+topic)

        
        print(self.config['favorites'])
        self.structure.update({
                'Continue' : {},
                'Favorites' : CardSession(self, self.config['favorites'], "favorites"),
                'View All Cards' : self.cards,
                #'Get More Cards' : self.getCards(),
                #'Save and Exit' : saveAndExit(),
                'Settings' : {
                # 'Check Server': line.checkServer()
                }
                
        })

        self.menu = Menu(
            structure = self.structure,
            lcd=lcd,
            idle_timeout=30
        )

        self.updateLastSession(self.config['lastSession'])

        touch.bind_defaults(self.menu)

    def formatCards(self, toLoad):
        cards = {}
        for pack in toLoad:
            if pack.split(".")[0] != "CONFIG":
                packContents = toLoad[pack]
                pack = pack.split(".")
                subject = pack[0]
                topic = pack[1]
                
                try:
                    cards[subject]
                except KeyError:
                    cards[subject] = {}
                
                cards[subject][topic] = packContents
        
        return cards

    def setLastSession(self, name):
        with open('local.json', "r+") as f:
            data = json.load(f)
            data['CONFIG']['lastSession'] = name
            self.config = data['CONFIG']
            f.seek(0)
            json.dump(data, f)
            f.truncate()

        self.updateLastSession(name)

    def updateLastSession(self, name):
        print(name)
        if name == "favorites":
            self.menu.menu_options['Continue'] = CardSession(self, self.config["favorites"], name, True)
            print("wut")
            print(self.menu.menu_options['Continue'].cards)
        else:
            subject = name.split('.')[0]
            topic = name.split('.')[1]
            self.menu.menu_options['Continue'] = self.cards[subject][topic]

    
    def favoriteCard(self, cardFront, cardBack, adding):
        if adding:
            if cardFront not in self.config['favorites']:
                with open('local.json', "r+") as f:
                    data = json.load(f)
                    data['CONFIG']['favorites'].update({cardFront:cardBack})
                    self.config = data['CONFIG']
                    f.seek(0)
                    json.dump(data, f)
                    f.truncate()
        else:
            if cardFront in self.config['favorites']:
                with open('local.json', "r+") as f:
                    data = json.load(f)
                    data['CONFIG']['favorites'].pop(cardFront)
                    self.config = data['CONFIG']
                    f.seek(0)
                    json.dump(data, f)
                    f.truncate()
        
        self.menu.menu_options['Favorites'] = CardSession(self, self.config["favorites"], 'favorites')
        
        print(self.config['favorites'])
    def saveAndExit(self):
        pass

    def getCards(self):
        pass

    def update(self):
        self.menu.redraw()

main = App()

while 1:
	main.update()
	time.sleep(0.05)
