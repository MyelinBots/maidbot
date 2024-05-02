import random
import sys

from pyircsdk import Module


class CakeModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "cake")
        self.cakes = [
            "Chocolate", 
            "Vanilla", 
            "Red Velvet", 
            "Carrot", 
            "Lemon", 
            "Coconut" ,
            "Marble" ,
            "Black Forest" ,
            "Coffee" ,
            "Banana" ,
            "Tiramisu" ,
            "Raspberry" ,
            "Matcha Green Tea"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                cake = random.choice(self.cakes)
                if command.args[0] in self.cakes:
                    cake = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "The maid serves a piece of %s cake to %s and hope you like it ^^" % (cake, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "The maid serves a piece of %s cake to %s and hope you like it ^^" % (cake, giveTo))
                
