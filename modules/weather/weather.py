import random
import sys
from datetime import time

from pyircsdk import Module

from .locations import Locations
from .weather_api import WeatherAPI


class WeatherModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "w")
        self.weatherApi = WeatherAPI()
        self.locations = Locations()


    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                message.messageFrom = message.messageFrom.lower()
                if self.locations.has_location(message.messageFrom) is False and len(command.args) == 0:
                    self.irc.privmsg(message.messageTo,
                                     "I am terribly sorry, but I am unable to find your location. Please add a location using !w add <location> or provide a location using !w <location>")
                    return
                if self.locations.has_location(message.messageFrom) and len(command.args) == 0:
                    location = self.locations.get_location(message.messageFrom)
                    if location != None:
                        weather = self.weatherApi.get_weather(location)
                        weatherMessage = ":: %s, %s, %s ::" % (weather.location.name, weather.location.region, weather.location.country)
                        weatherMessage += " :: Temperature %s °F | %s °C ::" % (weather.current.temp_f, weather.current.temp_c)
                        weatherMessage += " :: Pressure %s in | %s mb ::" % (weather.current.pressure_in, weather.current.pressure_mb)
                        weatherMessage += " :: Humidity %s ::" % weather.current.humidity
                        weatherMessage += " :: Percipitation %s in | %s mm ::" % (weather.current.precip_in, weather.current.precip_mm)
                        weatherMessage += " :: UV %s ::" % weather.current.uv
                        weatherMessage += " :: Last Updated %s ::" % weather.current.last_updated
                        self.irc.privmsg(message.messageTo, weatherMessage)
                        return
                if command.args[0] == "help":
                    self.irc.privmsg(message.messageTo, "Usage: !w <location> | !w add <location> | !w remove")
                    return
                if command.args[0] == "add":
                    # join the rest of the args to get the location
                    location = " ".join(command.args[1:])
                    self.locations.add_location(message.messageFrom, location)
                    self.irc.privmsg(message.messageTo, "Location %s added" % location)
                    return
                if command.args[0] == "remove":
                    self.locations.remove_location(message.messageFrom)
                    self.irc.privmsg(message.messageTo, "Location removed")
                    return

                if len(command.args) != 0:
                    location = " ".join(command.args)
                    weather = self.weatherApi.get_weather(location)
                    weatherMessage = ":: %s, %s, %s ::" % (weather.location.name, weather.location.region, weather.location.country)
                    weatherMessage += " :: Temperature %s °F | %s °C ::" % (weather.current.temp_f, weather.current.temp_c)
                    weatherMessage += " :: Pressure %s in | %s mb ::" % (weather.current.pressure_in, weather.current.pressure_mb)
                    weatherMessage += " :: Humidity %s ::" % weather.current.humidity
                    weatherMessage += " :: Percipitation %s in | %s mm ::" % (weather.current.precip_in, weather.current.precip_mm)
                    weatherMessage += " :: UV %s ::" % weather.current.uv
                    weatherMessage += " :: Last Updated %s ::" % weather.current.last_updated
                    self.irc.privmsg(message.messageTo, weatherMessage)



    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo,
                                 "Sorry, I was unable to handle your request. Please try again later.")
                return