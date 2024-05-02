import random
import sys

from pyircsdk import Module


class TeaModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "tea")
        self.teas = [
            "rose", 
            "lavender", 
            "oolong", 
            "ginger", 
            "turmeric", 
            "green" ,
            "chai" ,
            "herbal" ,
            "earl grey" ,
            "assam" ,
            "peppermint" ,
            "chamomile" ,
            "rooibos" ,
            "hibicus" ,
            "white" ,
            "longjing" ,
            "matcha" ,
            "black" ,
            "pu-erh"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                tea = random.choice(self.teas)
                if command.args[0] in self.teas:
                    tea = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "The maid hands a cup of %s tea to %s and hope you like it ^^" % (tea, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "The maid hands a cup of %s tea to %s and hope you like it ^^" % (tea, giveTo))
 
    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "The maid is sorry, but the tea is not available :(")
                return 


                
