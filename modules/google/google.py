from __future__ import annotations
import re, time, threading
from typing import Dict, List, Optional
from pyircsdk import Module

try:
    from googlesearch import search
except Exception:
    search = None # type: ignore

class GoogleModule(Module):
    """
    Command:
        !google <query>

    Optional env/params:
        results     -> how many results to print (default 1)
        cooldown_s  -> per-target cooldown seconds (default 6)
        lang        -> search language code (default "en")
    """
    CMD = re.compile(r"^!google\s+(.+)$", re.I)

    def __init__(self, irc, *, results: int = 1, cooldown_s: int = 6, lang: str = "en", warn_missing: bool = True):
        super().__init__(irc)
        self.results = max(1, int(results))
        self.cooldown_s = int(cooldown_s)
        self.lang = lang or "en"
        self.warn_missing = warn_missing
        self._cd: Dict[str, float] = {}

    def startListening(self):
        if hasattr(self.irc, "add_message_handler"):
            self.irc.add_message_handler("PRIVMSG", self._on_privmsg)
        elif hasattr(self.irc, "on"):
            self.irc.on("PRIVMSG", self._on_privmsg)
        elif hasattr(self.irc, "addListener"):
            self.irc.addListener("PRIVMSG", self._on_privmsg)
        else:
            try: super().startListening()
            except Exception: pass

    def _on_privmsg(self, prefix, command, params):
        nick = prefix.split("!")[0] if isinstance(prefix, str) else "user"
        target = params[0] if params else ""
        message = params[1] if params and len(params) > 1 else ""

        m = self.CMD.match((message or "").strip())
        if not m: return

        query = m.group(1).strip()
        if not query:
            self._say(target, f"{nick}: usage: !google <query>")
            return
        
        if self._cooldown(target): return

        threading.Thread(target=self._search_and_reply, args=(target, nick, query), daemon=True).start()

    def _cooldown(self, target: str) -> bool:
        now = time.time()
        last = self._cd.get(target, 0)
        if now - last < self.cooldown_s:
            return True
        self._cd[target] = now
        return False
    
    def _search_and_reply(self, target: str, nick: str, query: str):
        if search is None:
            if self.warn_missing:
                self._say(target, f"{nick}: google module missing dependencies, cannot search")
            return

        try:
            # returns generator of URLs
            urls: List[str] = list(search(query, num_results=self.results, lang=self.lang))
            if not urls:
                self._say(target, f"{nick}: no results for '{query}'.")
                return

            # Top result(s)
            for i, url in enumerate(urls, 1):
                if self.results == 1:
                    self._say(target, f"🔎 {url}")
                else:
                    self._say(target, f"🔎 {i}. {url}")
        except Exception as e:
            self._say(target, f"{nick}: error searching Google: {e}")

    def _say(self, target: str, text: str):
        try: self.privmsg(target, text)
        except AttributeError: self.irc.privmsg(target, text)
        
       
