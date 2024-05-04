from pyircsdk import IRCSDKConfig, IRCSDK, Module
import os

from modules.clean.clean import CleanModule
from modules.tea.tea import TeaModule
from modules.ramen.ramen import RamenModule
from modules.cake.cake import CakeModule
from modules.snack.snack import SnackModule
from modules.greeting.greeting import GreetingModule
from modules.drink.drink import DrinkModule

host = os.getenv('HOST', 'irc.rizon.net')
port = os.getenv('PORT', 6667)
port = str(port)
nick = os.getenv('NICK', 'Maid')
channel = os.getenv('CHANNEL', '#toolbot')
realname = os.getenv('REALNAME', 'Maid')

irc = IRCSDK(IRCSDKConfig(
    host,
    port,
    nick,
    channel,
    realname
))

teaModule = TeaModule(irc)
teaModule.startListening()

ramenModule = RamenModule(irc)
ramenModule.startListening()

cakeModule = CakeModule(irc)
cakeModule.startListening()

snackModule = SnackModule(irc)
snackModule.startListening()

greetingModule = GreetingModule(irc)
greetingModule.startListening()

cleanModule = CleanModule(irc)
cleanModule.startListening()

drinkModule = DrinkModule(irc)
drinkModule.startListening()

irc.connect(None)
