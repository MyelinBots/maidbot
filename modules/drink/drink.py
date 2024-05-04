import random
import sys

from pyircsdk import Module


class DrinkModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "drink")
        self.drinks = [
            "a glass of water", 
            "a glass of sparkling water", 
            "a glass of virgin mojito mocktail", 
            "a glass of virgin bloody mary mocktail", 
            "a glass of banana milkshake", 
            "a can of engery drink" ,
            "a cup of hot coffee" ,
            "a glass of Heineken beer" ,
            "a glass of red wine" ,
            "a glass of white wine" ,
            "a glass of lemon juice" ,
            "a glass of old fashioned cocktail" ,
            "a glass of dry martini cocktail" ,
            "a glass of margarita cocktail"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                drink = random.choice(self.drinks)
                if command.args[0] in self.drinks:
                    giveTo = command.args[0]
                    drink = command.args[1]
                    self.irc.privmsg(message.messageTo, "Here's your drink, the maid hands %s %s" % (giveTo, drink))
                    return
                
                self.irc.privmsg(message.messageTo, "Here's your drink, the maid hands %s %s" % (giveTo, drink))

    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Unfortunately, there are no drinks available right now. :(")
                return  