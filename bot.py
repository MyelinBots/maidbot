from pyircsdk import IRCSDKConfig, IRCSDK, Module

from modules.tea.tea import TeaModule
from modules.ramen.ramen import RamenModule
from modules.cake.cake import CakeModule
from modules.snack.snack import SnackModule
from modules.greeting.greeting import GreetingModule

irc = IRCSDK(IRCSDKConfig('irc.rizon.net',
                          6667,
                          'Maid',
                          '#toolbot',
                          'Maid'
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

irc.connect(None)