import random
import sys

from pyircsdk import Module


class SlapModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "slap")
        self.slaps = [
            "a soggy noodle", 
            "sandals",
            "a rubber chicken",
            "a designer’s guidebook 📘",
            "with a DVD case 📀",
            "a coffee mug ☕",
            "a large trout 🐟",
            "a keyboard ⌨️",
            "a pizza slice 🍕",
            "a meme handbook 📚",
            "a game controller 🎮",
            "a pillow 🛏️", 
            "a cupcake 🧁",
            "a laundry basket 🧺",
            "used undies",
            "her hand on the bum bum 🍑"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                if len(command.args) == 0:
                    slap = random.choice(self.slaps)
                    self.irc.privmsg(message.messageTo, "The maid slaps %s with %s" % (message.messageFrom, slap))
                    return

                giveTo = command.args[0]
                slap = random.choice(self.slaps)
                self.irc.privmsg(message.messageTo, "The maid slaps %s with %s" % (giveTo, slap))
                
    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Who do you want me to slap?")
                return 















                
