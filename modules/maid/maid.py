import random
import sys

from pyircsdk import Module


class MaidModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "maid")
        self.maids = [
            "straightens the sheets and arranges the pillows 🛏️🧴", 
            "changes the bed linens and fluffs the pillows 🛏️💐",
            "cleans the toilet until it sparkles 🚽✨",
            "scrubs the toilet and adds a fresh scent 🚽🧼",
            "scrubs and sanitizes the toilet thoroughly 🚽🧽",
            "removes stains and makes the toilet bowl gleam 🚽🌟",
            "carefully wipes down the laptop 💻🧼",
            "uses compressed air to remove crumbs from the keyboard ⌨️💨",
            "cleans the screen with a microfiber cloth 🖥️🧽",
            "sweeps and mops the floors 🧹🧼",
            "trims, waters, and beautifies the garden 🌿🌸",
            "does nothing",
            "cleans the room sparkling clean 🧹✨",
            "cleans up the living room efficiently 🧸🧹",
            "washes and polishes the car 🚗✨",
            "washes underwears 🩲🧼",
            "organizes the office meticulously 📂🧼",
            "scrubs the bathroom until it's spotless 🚿🧽",
            "takes the leash and heads out with the dog 🐾🚶‍♂️ 🐩 🐕 🦮",
            "dusts every corner thoroughly 🧽🌟",
            "organizes and cleans the desk 📚🧽",
            "cleans the windows until they're crystal clear 🧼🪟",
            "tidies up the kitchen 🍽️🧼",
            "washes, dries, and folds the laundry perfectly 🧺👚",
            "sorts and arranges the closet 👗🧹",
            "empties, cleans, and reorganizes the fridge 🧊🧼",
            "makes the bed and tidies up the guest room 🛏️🧹",
            "sorts, cleans, and organizes the garage 🧰🧽",
            "sweeps and cleans the patio 🍂🧹",
            "dusts and arranges the bookshelves 📚🧼",
            "cleans the mirror until it's crystal clear 🪞✨",
            "clears and cleans the dining table 🍽️🧹",
            "sweeps and dusts the hallway 🧹🐰",
            "organizes and cleans the pantry 🍞🧼",
            "helps organize and clean the attic 📦🧹",
            "cleans and sanitizes the counters 🧴🧽",
            "dusts, vacuums, and organizes the office 🖥️🧼",
            "sweeps and cleans the balcony 🍃🧼",
            "cleans and removes the stains from the rug 🧽🧼",
            "cleans the dishes and sanitizes the sink 🍽️🧽",
            "dusts and cleans the curtains 🧹🧼"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                maid = random.choice(self.maids)
                if command.args[0] in self.maids:
                    maid = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "The maid will take care of it, a maid %s for %s" % (maid, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "The maid will take care of it, a maid %s for %s" % (maid, giveTo))

    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Sorry, the maid can't do it because you forgot to pay her salary T_T")
                return