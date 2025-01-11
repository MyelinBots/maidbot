import random
import sys

from pyircsdk import Module


class FoodModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "food")
        self.foods = [
            "a piece of hawaiian pizza 🍕", 
            "a piece of new York Style pizza 🍕", 
            "a piece of greek pizza 🍕", 
            "a piece of margherita pizza 🍕", 
            "🍣 sushi rolls with assorted fillings", 
            "🌮 tacos filled with seasoned meat, lettuce, and cheese",
            "vanilla ice cream 🍦",
            "🥞 fluffy pancakes with syrup and butter",
            "a fruity 🍓 yogurt parfait",
            "🍦 creamy coconut ice cream cone with sprinkles",
            "🍝 spaghetti and meatballs",
            "nothing",
            "🍰 rich chocolate cake with frosting",
            "🍔 juicy cheeseburger with all the fixings", 
            "some crispy 🥒 cucumber slices with hummus",
            "🥗 fresh salad with mixed greens, tomatoes, and cucumbers",
            "🥪 grilled cheese sandwich with melted cheese",
            "🥐 croissant - buttery and flaky, perfect for breakfast or a snack",
            "🥙 falafel wrap - a delicious Middle Eastern treat with crispy falafel balls and fresh veggies",
            "🥪 panini - grilled sandwiches filled with tasty ingredients like cheese, meats, and veggies",
            "🍛 curry rice - flavorful curry sauce served over steamed rice",
            "🥟 dumplings - steamed or fried dough filled with savory fillings like chicken, or vegetables",
            "🍤 shrimp cocktail - chilled shrimp served with tangy cocktail sauce, a classic appetizer",
            "🍲 pho - vietnamese noodle soup with fragrant broth, rice noodles, and various meats or tofu",
            "🥗 cobb salad - a hearty salad made with mixed greens, grilled chicken, bacon, avocado, and blue cheese dressing",
            "🍳 eggs benedict - poached eggs on toasted English muffins with Canadian bacon and hollandaise sauce",
            "🍤 tempura - lightly battered and deep-fried seafood or vegetables",
            "🍛 bibimbap - a Korean rice dish topped with assorted vegetables, meat, a fried egg, and spicy gochujang sauce",
            "🍩 donuts - fried dough confections typically topped with icing, glaze, or sprinkles",
            "🍗 rotisserie chicken - tender and juicy chicken roasted on a spit, served with sides like potatoes or vegetables",
            "🌯 burrito - a Mexican dish consisting of a flour tortilla filled with rice, beans, meat, cheese, and other toppings",
            "🥧 apple pie - a classic dessert made with a flaky pastry crust and sweet apple filling, served with a scoop of ice cream",
            "🥞 belgian waffles - thick and fluffy waffles with deep pockets, typically served with syrup, fruit, or whipped cream",
            "🍱 bento box - a Japanese meal consisting of a compartmentalized box with rice, meat or fish, pickled vegetables",
            "🌭 hot dog - grilled or steamed sausage served in a sliced bun, often topped with mustard, ketchup, onions, or relish",
            "🍜 pad thai - a popular Thai stir-fried noodle dish made with rice noodles, tofu, eggs, peanuts, and tamarind sauce",
            "🥧 quiche lorraine - a savory French tart filled with eggs, cream, cheese, and bacon or ham",
            "🍨 affogato - an Italian dessert made by pouring hot espresso over a scoop of vanilla ice cream or gelato",
            "🍝 lasagna - layers of wide pasta sheets, meat sauce, ricotta cheese, and mozzarella, baked to perfection",
            "🍤 coconut shrimp - shrimp coated in a crispy batter made with shredded coconut, fried until golden brown and served with a dipping sauce",
            "🥣 clam chowder - a thick and creamy soup made with clams, potatoes, onions, and celery, served in a bread bowl",
            "🍛 butter chicken - a creamy and flavorful Indian dish made with marinated chicken cooked in a spiced tomato-based sauce"

        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                food = random.choice(self.foods)
                if command.args[0] in self.foods:
                    food = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "The maid gives %s to %s" % (food, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "The maid gives %s to %s" % (food, giveTo))
                
    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "The maid is sorry, but the fridge is empty :(")
                return 

                
