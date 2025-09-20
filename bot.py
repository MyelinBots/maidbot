from pyircsdk import IRCSDKConfig, IRCSDK, Module
import os

from modules.kiss.kiss import KissModule
from modules.slap.slap import SlapModule
from modules.hug.hug import HugModule
from modules.tea.tea import TeaModule
from modules.ramen.ramen import RamenModule
from modules.cake.cake import CakeModule
from modules.food.food import FoodModule
from modules.greeting.greeting import GreetingModule
from modules.drink.drink import DrinkModule
from modules.maid.maid import MaidModule
from modules.help.help import HelpModule
from modules.coffee.coffee import CoffeeModule
from modules.weather import locations
from modules.weather.weather import WeatherModule
from modules.horoscope.horoscope import HoroscopeModule
from modules.quote.quote import QuoteModule
from modules.snack.snack import SnackModule
from modules.time.time import TimeModule, TimezoneModule, Locations
from modules.invite.invite import InviteModule
from modules.youtube.youtube import YouTubeModule
from modules.google.google import GoogleModule



host = os.getenv('HOST', 'US.DarkWorld.Network')
port = os.getenv('PORT', '6697')
# convert port string to int
port = int(port)
nick = os.getenv('NICK', 'Maid')
ssl = os.getenv('SSL', 'True')
channel = os.getenv('CHANNEL', '#testing')
channels = os.getenv('CHANNELS', '#testing').split(',')
user = os.getenv('USER', 'Maid')
realname = os.getenv('REALNAME', 'Maid')
nickservFormat = os.getenv('NICKSERV_FORMAT', 'nickserv :identify %s')
nickservPassword = os.getenv('NICKSERV_PASSWORD', None)
passw = os.getenv('PASS', None)
nodataTimeout = os.getenv('NODATA_TIMEOUT', 120)
allowAnySSL = os.getenv('ALLOW_ANY_SSL', False)

irc = IRCSDK(IRCSDKConfig(
    host=host,
    port=port,
    nick=nick,
    ssl=ssl == 'True',
    channel=channel,
    channels=channels,
    user=user,
    realname=realname,
    nickservFormat=nickservFormat,
    nickservPassword=nickservPassword,
    password=passw,
    nodataTimeout=int(nodataTimeout),
    allowAnySSL=allowAnySSL == 'True'
))

teaModule = TeaModule(irc)
teaModule.startListening()

ramenModule = RamenModule(irc)
ramenModule.startListening()

cakeModule = CakeModule(irc)
cakeModule.startListening()

foodModule = FoodModule(irc)
foodModule.startListening()

# greetingModule = GreetingModule(irc)
# greetingModule.startListening()

maidModule = MaidModule(irc)
maidModule.startListening()

drinkModule = DrinkModule(irc)
drinkModule.startListening()

helpModule = HelpModule(irc)
helpModule.startListening()

coffeeModule = CoffeeModule(irc)
coffeeModule.startListening()

weatherModule = WeatherModule(irc)
weatherModule.startListening()

slapModule = SlapModule(irc)
slapModule.startListening()

kissModule = KissModule(irc)
kissModule.startListening()

hugModule = HugModule(irc)
hugModule.startListening()

horoscopeModule = HoroscopeModule(irc)
horoscopeModule.startListening()

quoteModule = QuoteModule(irc)
quoteModule.startListening()

snackModule = SnackModule(irc)
snackModule.startListening()

locations = Locations()

timeModule = TimeModule(irc, locations)
timeModule.startListening()

timezoneModule = TimezoneModule(irc, locations)
timezoneModule.startListening()

inviteModule = InviteModule(irc)
inviteModule.startListening()

youtubeModule = YouTubeModule(
    irc,
    default_results=1,
    cooldown_s=6,
    warn_missing=True
)
youtubeModule.startListening()

googleModule = GoogleModule(
    irc,
    default_results=int(os.getenv("GOOGLE_RESULTS", "1")),
    cooldown_s=int(os.getenv("GOOGLE_COOLDOWN", "6")),
    lang=os.getenv("GOOGLE_LANG", "en"),
)
googleModule.startListening()

irc.connect(None)
