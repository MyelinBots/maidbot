# stores the locations of nicks
class Locations:
    def __init__(self):
        self.locations = {}

    def add_location(self, nick, channel, location):
        nick = nick.lower()
        channel = channel.lower()
        print("Adding location", nick, channel, location)
        if channel not in self.locations:
            self.locations[channel] = {}
        self.locations[channel][nick] = location

    def get_location(self, nick, channel):
        nick = nick.lower()
        channel = channel.lower()
        print(nick, self.locations)
        if channel in self.locations:
            return self.locations[channel].get(nick, None)
        return None

    def remove_location(self, nick, channel):
        nick = nick.lower()
        channel = channel.lower()
        if channel in self.locations:
            self.locations[channel].pop(nick, None)

    def has_location(self, nick, channel) -> bool:
        # check if nick exists in locations
        nick = nick.lower()
        channel = channel.lower()
        if channel in self.locations:
            for key in self.locations[channel]:
                if key == nick:
                    print("Found location", nick, channel)
                    return True
        print("Location not found", nick, channel)
        return False

    def get_all_locations(self):
        return self.locations

    def clear(self):
        self.locations.clear()