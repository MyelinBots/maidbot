from __future__ import annotations
import threading
import time
import inspect
from typing import Dict, List, Optional, Tuple

from pyircsdk import Module

# -------- Optional backends (import if available) --------
try:
    from googlesearch import search as google_search_func  # pip install googlesearch-python
    GOOGLE_AVAILABLE = True
except Exception:
    google_search_func = None  # type: ignore
    GOOGLE_AVAILABLE = False

try:
    from duckduckgo_search import DDGS  # pip install duckduckgo-search
    DDG_AVAILABLE = True
except Exception:
    DDG_AVAILABLE = False

try:
    import requests  # used for Google CSE (official API)
    REQUESTS_AVAILABLE = True
except Exception:
    REQUESTS_AVAILABLE = False


class GoogleModule(Module):
    """
    Usage:
      !google <query>
      !google help
      !google set results <1-5>
      !google set cooldown <seconds>
      !google set lang <code>
      !google engine google|ddg|cse
      !google debug

    Notes:
      • Engine 'cse' requires Google Custom Search API key & CX (see _load_cse_config()).
      • Default results = 3 (minimum), max = 5.
    """
    MAX_RESULTS = 5
    UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    def __init__(self, irc, *, default_results: int = 3, cooldown_s: int = 6, lang: str = "en", warn_missing: bool = True):
        super().__init__(irc, "!", "google")
        self.results = max(3, min(int(default_results), self.MAX_RESULTS))  # minimum 3 as requested
        self.cooldown_s = int(cooldown_s)
        self.lang = (lang or "en").strip().lower()
        self.warn_missing = warn_missing
        self._cd: Dict[str, float] = {}

        # Choose default engine by availability (prefer ddg -> google -> none)
        if DDG_AVAILABLE:
            self.engine = "ddg"
        elif GOOGLE_AVAILABLE:
            self.engine = "google"
        else:
            self.engine = "none"

        # Load optional CSE config (google_api_key / google_cx on irc.config)
        self.cse_key, self.cse_cx = self._load_cse_config()

    # ========= WeatherModule-style entry points =========

    def handleCommand(self, message, command):
        if message.command != "PRIVMSG":
            return
        if command.command != self.fantasy + self.command:
            return

        frm = (message.messageFrom or "").lower()
        to = message.messageTo
        args = command.args or []

        # Help / no-args
        if len(args) == 0 or (len(args) == 1 and args[0].lower() == "help"):
            self._say(
                to,
                "Usage: !google <query> ::::: !google set results <1-5> ::::: !google set cooldown <seconds> ::::: "
                "!google set lang <code> ::::: !google engine google|ddg|cse ::::: !google debug"
            )
            return

        # Engine selection
        if args[0].lower() == "engine" and len(args) >= 2:
            eng = args[1].lower()
            if eng not in ("google", "ddg", "cse"):
                self._say(to, f"{frm}: engine must be 'google', 'ddg', or 'cse'")
                return
            if eng == "google" and not GOOGLE_AVAILABLE:
                self._say(to, f"{frm}: google scraping backend not available. (pip install googlesearch-python)")
                return
            if eng == "ddg" and not DDG_AVAILABLE:
                self._say(to, f"{frm}: ddg backend not available. (pip install duckduckgo-search)")
                return
            if eng == "cse":
                if not REQUESTS_AVAILABLE:
                    self._say(to, f"{frm}: requests not installed. (pip install requests)")
                    return
                if not (self.cse_key and self.cse_cx):
                    self._say(to, f"{frm}: CSE requires API key & CX. Set irc.config.google_api_key and irc.config.google_cx.")
                    return
            self.engine = eng
            self._say(to, f"OK {frm}: engine set to {self.engine}")
            return

        # Settings
        if args[0].lower() == "set" and len(args) >= 2:
            sub = args[1].lower()
            if sub == "results" and len(args) >= 3:
                try:
                    n = int(args[2])
                    self.results = max(3, min(n, self.MAX_RESULTS))  # keep minimum 3
                    self._say(to, f"OK {frm}: results set to {self.results}")
                except ValueError:
                    self._say(to, f"{frm}: results must be an integer 1..{self.MAX_RESULTS}")
                return
            if sub == "cooldown" and len(args) >= 3:
                try:
                    s = int(args[2])
                    self.cooldown_s = max(0, s)
                    self._say(to, f"OK {frm}: cooldown set to {self.cooldown_s}s")
                except ValueError:
                    self._say(to, f"{frm}: cooldown must be an integer (seconds)")
                return
            if sub == "lang" and len(args) >= 3:
                self.lang = args[2].strip().lower() or "en"
                self._say(to, f"OK {frm}: language set to {self.lang}")
                return
            self._say(to, "Usage: !google set results <1-5> ::::: !google set cooldown <seconds> ::::: !google set lang <code>")
            return

        # Debug
        if args[0].lower() == "debug":
            self._debug(to, frm)
            return

        # Regular search
        query = " ".join(args).strip()
        if not query:
            self._say(to, f"{frm}: usage: !google <query>")
            return
        if self._cooldown(to):
            return

        threading.Thread(target=self._search_and_reply, args=(to, frm, query), daemon=True).start()

    def handleError(self, message, command, error):
        if message.command == "PRIVMSG" and command.command == self.fantasy + self.command:
            self._say(message.messageTo, "Sorry, I was unable to handle your request. Please try again later.")
        try:
            print(error)
        except Exception:
            pass

    # ================= internals =================

    def _load_cse_config(self) -> Tuple[Optional[str], Optional[str]]:
        # Prefer values from irc.config if available; otherwise None
        key = getattr(getattr(self.irc, "config", object()), "google_api_key", None)
        cx  = getattr(getattr(self.irc, "config", object()), "google_cx", None)
        # Allow env-style fallbacks if you prefer:
        # import os
        # key = key or os.getenv("GOOGLE_API_KEY")
        # cx  = cx  or os.getenv("GOOGLE_CX")
        return key, cx

    def _debug(self, target: str, frm: str):
        parts = [
            f"engine={self.engine}",
            f"lang={self.lang}",
            f"results={self.results}",
            f"cooldown_s={self.cooldown_s}",
            f"cse_key_set={'yes' if self.cse_key else 'no'}",
            f"cse_cx_set={'yes' if self.cse_cx else 'no'}",
        ]
        if GOOGLE_AVAILABLE and google_search_func:
            try:
                parts.append(f"google_signature={inspect.signature(google_search_func)}")
            except Exception:
                parts.append("google_signature=?")
        parts.append(f"ddg_available={DDG_AVAILABLE}")
        parts.append(f"requests_available={REQUESTS_AVAILABLE}")
        self._say(target, f"{frm}: debug -> " + " | ".join(parts))

    def _cooldown(self, target: str) -> bool:
        now = time.time()
        last = self._cd.get(target, 0.0)
        if now - last < self.cooldown_s:
            return True
        self._cd[target] = now
        return False

    def _search_and_reply(self, target: str, nick: str, query: str):
        urls: List[str] = []
        titles: List[Optional[str]] = []
        err: Optional[Exception] = None

        # Preferred engine
        if self.engine == "cse" and self.cse_key and self.cse_cx and REQUESTS_AVAILABLE:
            urls, titles, err = self._try_cse(query)
        elif self.engine == "ddg" and DDG_AVAILABLE:
            urls, titles, err = self._try_ddg(query)
        elif self.engine == "google" and GOOGLE_AVAILABLE and google_search_func:
            urls, titles, err = self._try_google(query)

        # Fallbacks in priority order: ddg -> google -> cse (if configured)
        if not urls:
            if DDG_AVAILABLE and self.engine != "ddg":
                urls, titles, err2 = self._try_ddg(query)
                if urls:
                    err = err or err2
            if not urls and GOOGLE_AVAILABLE and google_search_func and self.engine != "google":
                urls, titles, err2 = self._try_google(query)
                if urls:
                    err = err or err2
            if not urls and self.cse_key and self.cse_cx and REQUESTS_AVAILABLE and self.engine != "cse":
                urls, titles, err2 = self._try_cse(query)
                if urls:
                    err = err or err2

        if not urls:
            if err:
                self._say(target, f"{nick}: search failed ({err}).")
            else:
                self._say(target, f"{nick}: no results for '{query}'.")
            return

        # Emit at least self.results items (min 3 by config)
        count = min(len(urls), self.results)
        for i in range(count):
            title = titles[i] if i < len(titles) else None
            if title:
                self._say(target, f"=== {i+1}. {title} • {urls[i]}")
            else:
                self._say(target, f"=== {i+1}. {urls[i]}")

    # --- backends ---

    def _try_google(self, query: str) -> Tuple[List[str], List[Optional[str]], Optional[Exception]]:
        urls: List[str] = []
        err: Optional[Exception] = None
        try:
            # Style B first (common): num/stop/pause/user_agent/lang/tld
            urls = list(google_search_func(
                query,
                num=self.results,
                stop=self.results,
                pause=2.0,
                user_agent=self.UA,
                lang=self.lang,
                tld="com",
            ))
        except TypeError:
            try:
                # Style A (some forks): num_results + lang
                urls = list(google_search_func(query, num_results=self.results, lang=self.lang))
            except Exception as e2:
                err = e2
        except Exception as e:
            err = e
        # scraping backend has no titles
        titles: List[Optional[str]] = [None] * len(urls)
        return urls, titles, err

    def _try_ddg(self, query: str) -> Tuple[List[str], List[Optional[str]], Optional[Exception]]:
        if not DDG_AVAILABLE:
            return [], [], None
        try:
            with DDGS() as ddgs:
                res = ddgs.text(query, max_results=self.results)
                urls = []
                titles: List[Optional[str]] = []
                for r in res:
                    link = r.get("href") or r.get("url")
                    if not link:
                        continue
                    urls.append(link)
                    titles.append(r.get("title"))
            return urls, titles, None
        except Exception as e:
            return [], [], e

    def _try_cse(self, query: str) -> Tuple[List[str], List[Optional[str]], Optional[Exception]]:
        if not (self.cse_key and self.cse_cx and REQUESTS_AVAILABLE):
            return [], [], None
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {"q": query, "cx": self.cse_cx, "key": self.cse_key, "num": self.results}
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            items = data.get("items", []) if isinstance(data, dict) else []
            urls = [it.get("link", "") for it in items if it.get("link")]
            titles = [it.get("title") for it in items]
            return urls, titles, None
        except Exception as e:
            return [], [], e

    def _say(self, target: str, text: str):
        try:
            self.irc.privmsg(target, text)
        except Exception:
            try:
                self.privmsg(target, text)
            except Exception:
                pass
