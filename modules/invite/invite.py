from pyircsdk import Module
import re

class InviteModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "invite")
        self.name = "InviteModule"
        self.description = "Handles the !invite command to invite maidbot to a channel."

    def is_valid_channel(self, channel):
        return re.match(r"^#[a-zA-Z0-9_]+$", channel) is not None

    def handle(self, channel, user, args):
        print(f"[DEBUG] Raw args before split: {args}")

        # Always split the first element if there's only one arg
        if len(args) == 1 and isinstance(args[0], str):
            args = args[0].strip().split()

        print(f"[DEBUG] Parsed args: {args}")

        if len(args) < 2 or args[0].lower() != "maid" or not self.is_valid_channel(args[1]):
            # No usage message here anymore
            print(f"[InviteModule] Invalid args from {user.nick}: {args}")
            return

        target_channel = args[1]
        self.irc.join(target_channel)
        self.irc.privmsg(
            target_channel,
            f"maidbot: bows gracefully and joins {user.nick}'s channel. How may I serve, ❤️~? 🫖"
        )
        print(f"[InviteModule] {user.nick} invited maidbot to {target_channel}")

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                print(f"[DEBUG] command.args: {command.args}")
                self.handle(message.messageTo, message.messageFrom, command.args)
