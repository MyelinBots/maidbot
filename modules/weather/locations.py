# stores the locations of nicks
class Locations:
    def __init__(self):
        self.locations = {}

    def add_location(self, nick, channel, location):
        print("Adding location", nick, channel, location)
        if channel not in self.locations:
            self.locations[channel] = {}
        print("contiuining")
        self.locations[channel][nick] = location

    def get_location(self, nick, channel):
        print(nick, self.locations)
        if channel in self.locations:
            return self.locations[channel].get(nick, None)
        return None

    def remove_location(self, nick, channel):
        if channel in self.locations:
            self.locations[channel].pop(nick, None)

    def has_location(self, nick, channel) -> bool:
        # check if nick exists in locations
        if channel in self.locations:
            return nick in self.locations[channel]
        return False

    def get_all_locations(self):
        return self.locations

    def clear(self):
        self.locations.clear()