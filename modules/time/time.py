import pytz
from datetime import datetime
from pyircsdk import Module

class TimeModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "time")
        self.locations = Locations()  # Store user-set locations

    def get_time(self, location):
        """Returns the current time for a given location."""
        try:
            now = datetime.now(pytz.timezone(location)).strftime('%H:%M')
            return f"{location} Time: {now}"
        except pytz.UnknownTimeZoneError:
            return "Invalid timezone. Please enter a valid timezone from the IANA database (e.g., America/New_York, Asia/Bangkok)."

    def handleCommand(self, message, command):
        """Handles the !time command."""
        user_location = self.locations.get_location(message.nick, message.messageTo)

        if user_location:
            self.irc.privmsg(message.messageTo, self.get_time(user_location))
        else:
            self.irc.privmsg(message.messageTo, f"{message.nick}, you haven't set a timezone. Use !timezone set <timezone>.")

    def handleError(self, message, command, error):
        """Handles errors gracefully."""
        print(error)
        if message.command == "PRIVMSG" and command.command == self.fantasy + self.command:
            self.irc.privmsg(message.messageTo, "Sorry, I encountered an error. Please try again later.")

class TimezoneModule(Module):
    def __init__(self, irc, locations):
        super().__init__(irc, "!", "timezone")
        self.locations = locations  # Use shared location storage

    def handleCommand(self, message, command):
        """Handles the !timezone command."""
        args = command.args.split()

        if not args:
            self.irc.privmsg(message.messageTo, "Usage: !timezone list | !timezone set <timezone> | !timezone remove")
            return

        subcommand = args[0].lower()

        if subcommand == "list":
            self.show_timezone_list(message)
        
        elif subcommand == "set" and len(args) > 1:
            location = " ".join(args[1:])
            if location in pytz.all_timezones:
                self.locations.add_location(message.nick, message.messageTo, location)
                self.irc.privmsg(message.messageTo, f"{message.nick}, your timezone has been set to {location}.")
            else:
                self.irc.privmsg(message.messageTo, "Invalid timezone. Use !timezone list to see available timezones.")

        elif subcommand == "remove":
            self.locations.remove_location(message.nick, message.messageTo)
            self.irc.privmsg(message.messageTo, f"{message.nick}, your timezone has been removed.")

        else:
            self.irc.privmsg(message.messageTo, "Invalid command. Use !timezone list | !timezone set <timezone> | !timezone remove")

    def show_timezone_list(self, message):
        """Displays available timezones grouped by continent."""
        timezones_by_continent = {}
        for tz in pytz.all_timezones:
            continent = tz.split('/')[0]
            if continent not in timezones_by_continent:
                timezones_by_continent[continent] = []
            timezones_by_continent[continent].append(tz)

        for continent, timezones in timezones_by_continent.items():
            self.irc.privmsg(message.messageTo, f"{continent}: {', '.join(timezones[:10])}... (use full name)")

class Locations:
    """Stores the timezone locations of users in channels."""
    
    def __init__(self):
        self.locations = {}

    def add_location(self, nick, channel, location):
        """Adds or updates a user's location."""
        nick = nick.lower()
        channel = channel.lower()
        print("Adding location:", nick, channel, location)
        if channel not in self.locations:
            self.locations[channel] = {}
        self.locations[channel][nick] = location

    def get_location(self, nick, channel):
        """Retrieves a user's location or None if not set."""
        nick = nick.lower()
        channel = channel.lower()
        return self.locations.get(channel, {}).get(nick)

    def remove_location(self, nick, channel):
        """Removes a user's location."""
        nick = nick.lower()
        channel = channel.lower()
        if channel in self.locations and nick in self.locations[channel]:
            del self.locations[channel][nick]

    def get_all_locations(self):
        """Returns all stored locations."""
        return self.locations

    def clear(self):
        """Clears all stored locations."""
        self.locations.clear()
