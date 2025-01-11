import random
import sys

from pyircsdk import Module


class QuoteModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "quote")
        
        self.quotes = [
            "If I were a vegetable, I’d be a cute-cumber. 🥒" , 
            "I’m on a seafood diet. I see food, and I eat it. 🍔" , 
            "I’m not arguing, I’m just explaining why I’m right." , 
            "I’m writing a book. I’ve got the page numbers done." , 
            "I used to be indecisive, but now I’m not so sure." ,
            "I'm on a whiskey diet. I’ve lost three days already." ,
            "I’m not lazy, I’m just on energy-saving mode." ,
            "My wallet is like an onion. When I open it, it makes me cry." ,
            "I’m great at multitasking. I can waste time, be unproductive, and procrastinate all at once." ,
            "Some people graduate with honors, I am just honored to graduate.",
            "I put my phone in airplane mode, but it’s not flying! ✈️ ",
            "I don’t need a hairstylist. My pillow gives me a new look every morning. 🛌 ",
            "I thought about losing weight once... but I don’t like losing. 🏆"

        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                quote = random.choice(self.quotes)
                if command.args[0] in self.quotes:
                    quote = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "Today's quote for %s is * %s * " % (giveTo, quote))
                    return
                
                self.irc.privmsg(message.messageTo, "Today's quote for %s is * %s * " % (giveTo, quote))
 
    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Error 404: Motivation Not Found. Please try coffee and try again. ☕ :(")
                return 


                
