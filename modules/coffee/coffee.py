import random
import sys

from pyircsdk import Module


class CoffeeModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "coffee")
        self.coffees = [
            "a cup of cappuccino ☕️🥛, an espresso-based drink topped with steamed milk foam, offering a creamy texture and balanced flavor", 
            "a cup of macchiato: ☕️🥛, an espresso with a small amount of steamed milk or milk foam, creating a bold coffee flavor with a hint of creaminess", 
            "a cup of americano ☕️💧, a simple yet bold coffee made by diluting espresso with hot water, resulting in a smooth and rich cup", 
            "a cup of flat White ☕️🥛, a velvety espresso drink topped with a thin layer of microfoam milk, offering a smooth and indulgent texture", 
            "a cup of espresso ☕️, strong and intense, perfect for a quick caffeine boost", 
            "a cup of mocha ☕️🍫, a decadent coffee drink made with espresso, steamed milk, and chocolate syrup or cocoa powder, perfect for chocolate lover",
            "a glass of vietnamese iced coffee, ☕️🇻🇳 strong and sweet coffee brewed with dark roast coffee and condensed milk, poured over ice for a refreshing and indulgent treat",
            "a glass of affogato ☕️🍨, a delightful dessert featuring a scoop of vanilla ice cream or gelato in a shot of hot espresso, creating a delicious contrast of hot and cold",
            "a glass of iced coffee ☕️❄️, chilled coffee served over ice, perfect for hot summer days or as a refreshing pick-me-up any time of yea",
            "a cup of irish coffee ☕️🥃, a cozy cocktail made with hot coffee, Irish whiskey, sugar, and topped with a dollop of whipped cream, perfect for warming up on a chilly evening",
            "a cup of turkish coffee ☕️🇹🇷, a traditional method of preparing coffee by boiling finely ground coffee beans with sugar and water in a special pot called a cezve, resulting in a strong and aromatic brew",
            "a cup of flat black coffee ☕️🖤, a simple and straightforward black coffee without any milk or sugar, highlighting the natural flavors and aromas of the coffee beans",
            "a cup of hazelnut latte ☕️🌰, a velvety latte flavored with rich hazelnut syrup, perfect for those who enjoy a nutty and aromatic twist to their coffee"

        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                coffee = random.choice(self.coffees)
                if command.args[0] in self.coffees:
                    giveTo = command.args[0]
                    coffee = command.args[1]
                    self.irc.privmsg(message.messageTo, "Here's your coffee, the maid hands %s %s ☕️" % (giveTo, coffee))
                    return
                
                self.irc.privmsg(message.messageTo, "Here's your coffee, the maid hands %s %s ☕️" % (giveTo, coffee))

    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "The coffee machine is out of service :P")
                return
