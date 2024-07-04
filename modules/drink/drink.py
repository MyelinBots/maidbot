import random
import sys

from pyircsdk import Module


class DrinkModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "drink")
        self.drinks = [
            "a glass of water 🥛", 
            "a glass of sparkling water 🥛", 
            "a glass of virgin mojito mocktail 🍸", 
            "a glass of virgin bloody mary mocktail 🍸", 
            "a glass of banana milkshake 🥛", 
            "a can of engery drink 🥤",
            "a glass of Heineken beer 🍺",
            "a can of asahi beer 🍺" , 
            "a glass of red wine 🍷",
            "a glass of white wine 🍷",
            "a glass of lemon juice 🧃",
            "a glass of orange juice 🧃",
            "a glass of apple juice 🧃", 
            "a glass of old fashioned cocktail 🍸",
            "a glass of dry martini cocktail 🍸",
            "a glass of margarita cocktail 🍸", 
            "a glass of espresso martini ☕️🍸", 
            "a glass of mai tai 🍸", 
            "a glass of rum old fashioned 🍸", 
            "a glass of pina colada 🍸",
            "a glass of long island lced tea 🫖🍸", 
            "a glass of coconut milk 🥛", 
            "a can of dr. pepper 🥫", 
            "a glass of root beer 🥤",
            "a can of pepsi 🥫",
            "a can of dr.pepper 🥫",
            "a can of coca-cola 🥫"
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