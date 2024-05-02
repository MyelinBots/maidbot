import random
import sys

from pyircsdk import Module


class RamenModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "ramen")
        self.ramens = [
            "Tonkotsu", 
            "Miso", 
            "Shoyu", 
            "Shio", 
            "Tsukemen", 
            "Kagoshima" ,
            "Hakata" ,
            "Supporo" ,
            "Ramyoen" ,
            "Wakayama" ,
            "Okianawa" ,
            "Hakodate" 
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                ramen = random.choice(self.ramens)
                if command.args[0] in self.ramens:
                    ramen = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "The maid serves %s ramen to %s and enjoy eating :)" % (ramen, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "The maid serves %s ramen to %s and enjoy eating :)" % (ramen, giveTo))
                
    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "The maid is sorry, but the ramen is not available :(")
                return
        
        
                
