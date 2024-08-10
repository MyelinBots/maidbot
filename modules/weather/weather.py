import random
import sys
from datetime import time

from pyircsdk import Module

from modules.db.db import DB
from modules.db.weather import Weather
from modules.db.weather_repository import WeatherRepository

from .locations import Locations
from .weather_api import WeatherAPI


class WeatherModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "w")
        self.weatherApi = WeatherAPI()
        self.locations = Locations()
        self.db = DB()
        self.weatherRepository = WeatherRepository(self.db)
        self.syncWeathers()

    def syncWeathers(self):
        dbLocations: list[Weather] = self.weatherRepository.getAll()
        channels = []
        if self.irc.config.channels is not None and len(self.irc.config.channels) > 0:
            channels = self.irc.config.channels 
        else:
            channels = [self.irc.config.channel]
        for location in dbLocations:
            if location is None:
                continue
            if location.server != self.irc.config.host:
                continue
            if location.channel not in channels:
                continue
            self.locations.add_location(location.nick, location.channel, location.location)

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                message.messageFrom = message.messageFrom.lower()
                if self.locations.has_location(message.messageFrom, message.messageTo) is False and len(command.args) == 0:
                    self.irc.privmsg(message.messageTo,
                                     "I am terribly sorry, but I am unable to find your location. Please add a location using !w add <location> or provide a location using !w <location>")
                    return
                if self.locations.has_location(message.messageFrom, message.messageTo) and len(command.args) == 0:
                    location = self.locations.get_location(message.messageFrom, message.messageTo)
                    if location != None:
                        weather = self.weatherApi.get_weather(location)
                        weatherMessage = ":: %s, %s, %s ::" % (weather.location.name, weather.location.region, weather.location.country)
                        weatherMessage += " :: Temperature %s °F | %s °C ::" % (weather.current.temp_f, weather.current.temp_c)
                        weatherMessage += " :: Condition %s" % (weather.current.condition.text)
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
                    self.locations.add_location(message.messageFrom, message.messageTo, location)
                    self.weatherRepository.upsert(message.messageFrom, self.irc.config.host, message.messageTo, location)
                    self.irc.privmsg(message.messageTo, "Location %s added" % location)
                    return
                if command.args[0] == "remove":
                    self.locations.remove_location(message.messageFrom, message.messageTo)
                    self.weatherRepository.delete(message.messageFrom, self.irc.config.host, message.messageTo)
                    self.irc.privmsg(message.messageTo, "Location removed")
                    return

                if len(command.args) != 0:
                    location = " ".join(command.args)
                    weather = self.weatherApi.get_weather(location)
                    weatherMessage = ":: %s, %s, %s ::" % (weather.location.name, weather.location.region, weather.location.country)
                    weatherMessage += " :: Temperature %s °F | %s °C" % (weather.current.temp_f, weather.current.temp_c)
                    weatherMessage += " :: Condition: %s" % (weather.current.condition.text)
                    weatherMessage += " :: Pressure %s in | %s mb" % (weather.current.pressure_in, weather.current.pressure_mb)
                    weatherMessage += " :: Humidity %s" % weather.current.humidity
                    weatherMessage += " :: Percipitation %s in | %s mm" % (weather.current.precip_in, weather.current.precip_mm)
                    weatherMessage += " :: UV %s" % weather.current.uv
                    weatherMessage += " :: Last Updated %s ::" % weather.current.last_updated
                    self.irc.privmsg(message.messageTo, weatherMessage)



    def handleError(self, message, command, error):
        print(error)
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo,
                                 "Sorry, I was unable to handle your request. Please try again later.")
                return