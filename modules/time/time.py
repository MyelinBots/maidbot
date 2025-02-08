import pytz
from datetime import datetime
from pyircsdk import Module

class TimeModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "time")
        self.timezones = {
            "Bangkok": "Asia/Bangkok",
            "Berlin": "Europe/Berlin",
            "California": "America/Los_Angeles",
            "Dubai": "Asia/Dubai",
            "Dublin": "Europe/Dublin",
            "Islamabad": "Asia/Karachi",
            "Jakarta": "Asia/Jakarta",
            "Johannesburg": "Africa/Johannesburg",
            "Miami": "America/New_York",
            "Moscow": "Europe/Moscow",
            "Rio de Janeiro": "America/Sao_Paulo",
            "Sydney": "Australia/Sydney",
            "Taipei": "Asia/Taipei",
            "Tokyo": "Asia/Tokyo",
            "Vancouver": "America/Vancouver"
        }

    def get_time(self):
        time_results = []
        for city, tz in sorted(self.timezones.items()):
            now = datetime.now(pytz.timezone(tz)).strftime('%H:%M')
            time_results.append(f"{city} ({now})")
        return " :::: ".join(time_results)

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG" and command.command == self.fantasy + self.command:
            self.irc.privmsg(message.messageTo, self.get_time())

    def handleError(self, message, command, error):
        print(error)
        if message.command == "PRIVMSG" and command.command == self.fantasy + self.command:
            self.irc.privmsg(message.messageTo, "Sorry, I was unable to handle your request. Please try again later.")
