import random
import sys

from pyircsdk import Module


class TeaModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "tea")
        self.teas = [
            "rose tea 🌹, this delicate and aromatic beverage offers a subtle floral flavor and a soothing experience" , 
            "lavender tea ☕️, this calming herbal infusion offers a gentle floral aroma and a relaxing experience, perfect for unwinding after a busy day" , 
            "oolong tea 🍵, with its unique taste profile ranging from floral to nutty" , 
            "ginger tea ☕️, this spicy and invigorating brew is perfect for soothing the stomach and providing a comforting pick-me-up on a chilly day" , 
            "aromatic green tea 🍵, it's refreshing and packed with antioxidants!" ,
            "chai tea ☕️, it's blend of spices like cinnamon, cardamom, and cloves creates a warm and comforting beverage perfect for any time of day" ,
            "earl grey tea ☕️, it's distinctive flavor of bergamot is both calming and invigorating" ,
            "peppermint tea 🌿, refreshing and minty, perfect for aiding digestion and freshening breath" ,
            "hibiscus tea 🌺, tangy and floral, known for its vibrant color and potential health benefits like lowering blood pressure" ,
            "jasmine tea 🌼, fragrant and floral, with delicate jasmine blossoms infusing the tea leaves for a subtly sweet taste" ,
            "chamomile lavender tea 🌼💜, a calming blend of chamomile and lavender flowers, perfect for relaxation and promoting sleep" ,
            "white tea 🍃 , light and delicate, with a subtle sweetness and minimal processing, preserving its natural antioxidants" ,
            "Turmeric tea 🧡, warm and spicy" ,
            "rooibos tea 🍂, a caffeine-free herbal tea from South Africa, with a slightly sweet and nutty flavor profile" ,
            "cinnamon spice tea 🍂🌶️, a warm and comforting blend of black tea with cinnamon, cloves, and other spices, reminiscent of cozy autumn days" ,
            "ginseng oolong tea 🌱🍵, a unique combination of oolong tea with the earthy sweetness of ginseng" 
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                tea = random.choice(self.teas)
                if command.args[0] in self.teas:
                    tea = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "The maid hands a cup of %s to %s and hope you like it ^^" % (tea, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "The maid hands a cup of %s to %s and hope you like it ^^" % (tea, giveTo))
 
    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "The maid is sorry, but the tea is not available :(")
                return 


                
