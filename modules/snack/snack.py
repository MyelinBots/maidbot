import random
import sys

from pyircsdk import Module


class SnackModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "snack")
        self.snacks = [
            "a piece of hawaiian pizza", 
            "a piece of new York Style pizza", 
            "a piece of greek pizza", 
            "a piece of margherita pizza!", 
            "a can of pepsi", 
            "a can of coca-cola",
            "popcorn",
            "vanilla ice cream",
            "rainbow ice cream",
            "chocolate ice cream",
            "coconut ice cream",
            "strawberry ice cream",
            "nothing",
            "kit kat",
            "ferrero rocher",
            "lays chips",
            "marshmallow",
            "hamburger", 
            "fried chicken"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                snack = random.choice(self.snacks)
                if command.args[0] in self.snacks:
                    snack = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "The maid gives %s to %s" % (snack, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "The maid gives %s to %s" % (snack, giveTo))
                
    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "The maid is sorry, but the fridge is empty :(")
                return 

                
