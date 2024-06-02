
# stores the locations of nicks
class Locations:
    def __init__(self):
        self.locations = {}

    def add_location(self, nick, location):
        self.locations[nick] = location

    def get_location(self, nick):
        print(nick, self.locations)
        if nick in self.locations:
            return self.locations[nick]
        return None

    def remove_location(self, nick):
        self.locations.pop(nick, None)

    def has_location(self, nick) -> bool:
        # check if nick exists in locations
        if nick in self.locations:
            return True
        return False

    def get_all_locations(self):
        return self.locations

    def clear(self):
        self.locations.clear()
