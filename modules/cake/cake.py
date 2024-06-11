import random
import sys

from pyircsdk import Module


class CakeModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "cake")
        self.cakes = [
            "chocolate", 
            "vanilla", 
            "red velvet", 
            "carrot", 
            "lemon", 
            "coconut" ,
            "marble" ,
            "black forest" ,
            "coffee" ,
            "banana" ,
            "tiramisu" ,
            "raspberry" ,
            "matcha green tea"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                cake = random.choice(self.cakes)
                if command.args[0] in self.cakes:
                    cake = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "The maid serves a piece of %s cake 🍰 to %s and hope you like it ^^" % (cake, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "The maid serves a piece of %s cake 🍰 to %s and hope you like it ^^" % (cake, giveTo))

    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "The maid is sorry, but the cake is not available :(")
                return  
