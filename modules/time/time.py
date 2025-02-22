import pytz
from datetime import datetime
from pyircsdk import Module

class TimeModule(Module):
    def __init__(self, irc, locations):
        super().__init__(irc, "!", "time")
        self.locations = locations  # Shared instance

    def get_time(self, location):
        """Returns the current time for a given location."""
        if not location:
            return "No timezone set. Use !timezone set <timezone>."

        try:
            now = datetime.now(pytz.timezone(location)).strftime('%H:%M')
            return f"{location} Time: {now}"
        except pytz.UnknownTimeZoneError:
            return "Invalid timezone stored. Please set a new timezone using !timezone set <timezone>."

    def handleCommand(self, message, command):
        """Handles the !time command."""
        if message.command == "PRIVMSG" and command.command == self.fantasy + self.command:
            user_location = self.locations.get_location(message.messageFrom, message.messageTo)

            if user_location:
                self.irc.privmsg(message.messageTo, self.get_time(user_location))
            else:
                self.irc.privmsg(message.messageTo, f"{message.messageFrom}, you haven't set a timezone. Use !timezone set <timezone>.")

class TimezoneModule(Module):
    def __init__(self, irc, locations):
        super().__init__(irc, "!", "timezone")
        self.locations = locations  # Shared instance

    def handleCommand(self, message, command):
        """Handles the !timezone command."""
        if message.command == "PRIVMSG" and command.command == self.fantasy + self.command:
            if command.args[0] == "set":
                location = " ".join(command.args[1:])
                if location in pytz.all_timezones:
                    self.locations.add_location(message.messageFrom, message.messageTo, location)
                    self.irc.privmsg(message.messageTo, f"{message.messageFrom}, your timezone has been set to {location}.")
                else:
                    self.irc.privmsg(message.messageTo, "Invalid timezone. Use !timezone list to see available timezones.")
            if command.args[0] == "list":
                continent = command.args[1].capitalize() if len(command.args) > 1 else None
                self.show_timezone_list(message, continent)

    def show_timezone_list(self, message, continent=None):
        """Displays available timezones grouped by continent."""
        timezones_by_continent = {}
        for tz in pytz.all_timezones:
            zone_continent = tz.split('/')[0]
            if zone_continent not in timezones_by_continent:
                timezones_by_continent[zone_continent] = []
            timezones_by_continent[zone_continent].append(tz)

        if continent:
            # Show only timezones from the specified continent
            if continent in timezones_by_continent:
                timezones = timezones_by_continent[continent]
                chunks = [timezones[i:i + 10] for i in range(0, len(timezones), 10)]  # Split into chunks of 10
                for chunk in chunks[:3]:  # Only send up to 3 messages to prevent flooding
                    self.irc.privmsg(message.messageTo, f"{continent}: {', '.join(chunk)}")
            else:
                self.irc.privmsg(message.messageTo, "Invalid continent. Try: Africa, America, Asia, Europe, Pacific, etc.")
        else:
            # Show available continents
            self.irc.privmsg(message.messageTo, "Available continents: " + ", ".join(timezones_by_continent.keys()))
            self.irc.privmsg(message.messageTo, "Use !timezone list <continent> to see available timezones.")

class Locations:
    """Stores the timezone locations of users in channels."""
    
    def __init__(self):
        self.locations = {}

    def add_location(self, nick, channel, location):
        """Adds or updates a user's location."""
        nick = nick.lower()
        channel = channel.lower()
        if channel not in self.locations:
            self.locations[channel] = {}
        self.locations[channel][nick] = location

    def get_location(self, nick, channel):
        nick = nick.lower()
        """Retrieves a user's location or None if not set."""
        return self.locations.get(channel, {}).get(nick)

    def remove_location(self, nick, channel):
        """Removes a user's location."""
        if channel in self.locations and nick in self.locations[channel]:
            del self.locations[channel][nick]

    def get_all_locations(self):
        """Returns all stored locations."""
        return self.locations

    def clear(self):
        """Clears all stored locations."""
        self.locations.clear()
