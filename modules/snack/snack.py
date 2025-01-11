import random
import sys

from pyircsdk import Module


class SnackModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "snack")
        self.snacks = [
            "nothing",
            "a Kit Kat chocolate bar 🍫 with its crisp wafer layers covered in smooth milk chocolate",
            "classic Lay's potato chips 🥔🍟 - crispy, salty, and perfect",
            "Marshmallow 🍡",
            "Doritos Nacho Cheese 🌽🧀 - bold, cheesy, and dangerously crunchy",
            "Oreos 🍪🥛 - creamy filling and crispy cookies, perfect for dunking.",
            "Pringles Sour Cream & Onion 🥔🧅 - stacked chips with a tangy twist",
            "Cheetos Flamin' Hot 🔥🧀 - spicy, cheesy, and addictively good.",
            "Twix 🍫🍪 - chocolate, caramel, and cookie—snap into it!",
            "Popcorn 🍿 - buttery, fluffy, and made for movie nights.",
            "M&Ms 🍫🌈 - colorful candy-coated chocolate happiness.",
            "Snickers 🍫🥜 - satisfy your hunger with this nutty, caramel treat.",
            "Takis 🌶️ - rolled tortilla chips packed with fiery flavor.",
            "Ritz Crackers 🧂🍪 - buttery, flaky, and perfect for snacking or stacking.",
            "Goldfish Crackers 🧀🐟 - cheesy, bite-sized, and always smiling back.",
            "Honey Roasted Peanuts 🥜🍯 - sweet, salty, and totally addictive.",
            "Pocky Sticks 🍫🍓 - slim, crunchy sticks coated in creamy delight.",
            "Trail Mix 🌰🍇 - a mix of nuts, dried fruit, and chocolate for an energy boost.",
            "Pretzels 🥨 - twisted, salty, and satisfyingly crunchy.",
            "MoonPie 🍪🍫 - marshmallow-filled goodness, like a hug for your taste buds.",
            "nothing"
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

                
