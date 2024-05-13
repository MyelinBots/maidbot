import random
import sys

from pyircsdk import Module


class CoffeeModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "coffee")
        self.coffees = [
            "a cup of cappuccino", 
            "a cup of latte", 
            "a cup of americano", 
            "a cup of caffe macchiato", 
            "a cup of espresso", 
            "a cup of flat white" ,
            "a cup of cortado" ,
            "a cup of cafe mocha" ,
            "a glass of affogato" ,
            "a glass of cold brew" ,
            "a cup of doppio of " ,
            "a glass of iced coffee" ,
            "a cup of cafe au lait" ,
            "a glass of ristretto" ,
            "a cup of black coffee" ,
            "a cup of irish coffee" ,
            "a cup of long black" ,
            "a glass of frappe coffee" ,
            "a cup of turkish coffee"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                coffee = random.choice(self.coffees)
                if command.args[0] in self.coffees:
                    giveTo = command.args[0]
                    coffee = command.args[1]
                    self.irc.privmsg(message.messageTo, "Here's your coffee, sweetheart, the maid hands %s %s" % (giveTo, coffee))
                    return
                
                self.irc.privmsg(message.messageTo, "Here's your coffee, sweetheart, the maid hands %s %s" % (giveTo, coffee))

    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "The coffee machine is out of service :P")
                return  