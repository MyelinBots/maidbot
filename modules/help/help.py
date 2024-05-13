import sys
import json

from pyircsdk import Module


class HelpModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "help")

    def handleCommand(self, message, messegeTo):
        if command.command == "PRIVMSG":
           if command.command == self.fantasy + self.command:

                    self.irc.privmsg(message.messegeTo, "Hello, %s, these are available commands; !cake <nick> !drink <nick> !maid <nick> !ramen <nick> !snack <nick> !tea <nick>" % message.messageFrom)
                    self.irc.privmsg(message.messegeTo, "To play pigeon game; !shoot and to check score; !score")
                    return
   
                  
                         