from pyircsdk import IRCSDKConfig, IRCSDK, Module
import os

from modules.tea.tea import TeaModule
from modules.ramen.ramen import RamenModule
from modules.cake.cake import CakeModule
from modules.snack.snack import SnackModule
from modules.greeting.greeting import GreetingModule
from modules.drink.drink import DrinkModule
from modules.maid.maid import MaidModule
from modules.help.help import HelpModule

host = os.getenv('HOST', 'irc.rizon.net')
port = os.getenv('PORT', '6667')
# convert port string to int
port = int(port)
nick = os.getenv('NICK', 'Maid')
ssl = os.getenv('SSL', 'False')
channel = os.getenv('CHANNEL', '#toolbot')
user = os.getenv('USER', 'Maid')
realname = os.getenv('REALNAME', 'Maid')
nickservFormat = os.getenv('NICKSERV_FORMAT', 'nickserv :identify %s')
nickservPassword = os.getenv('NICKSERV_PASSWORD', None)
passw = os.getenv('PASS', None)

irc = IRCSDK(IRCSDKConfig(
    host=host,
    port=port,
    nick=nick,
    ssl=ssl == 'True',
    channel=channel,
    user=user,
    realname=realname,
    nickservFormat=nickservFormat,
    nickservPassword=nickservPassword,
    password=passw
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

maidModule = MaidModule(irc)
maidModule.startListening()

drinkModule = DrinkModule(irc)
drinkModule.startListening()

helpModule = HelpModule(irc)
helpModule.startListening()

irc.connect(None)