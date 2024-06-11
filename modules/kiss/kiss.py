import random
import sys

from pyircsdk import Module


class KissModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "kiss")
        self.kisss = [
            "on the cheek 😘",
            "on the forehead 💋",
            "on the nose ☕❤️",
            "on the lips 😘",
            "on the hand 🤗💋",
            "passionately 💞💋",
            "for good luck 🍀💋"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                if len(command.args) == 0:
                    kiss = random.choice(self.kisss)
                    self.irc.privmsg(message.messageTo, "kisses %s %s" % (message.messageFrom, kiss))
                    return

                giveTo = command.args[0]
                kiss = random.choice(self.kisss)
                self.irc.privmsg(message.messageTo, "kisses %s %s" % (giveTo, kiss))
                
    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Who do you want to kiss?")
                return 

  
                
















                
