from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass
from typing import Optional, List, Dict

from pyircsdk import Module

try:
    from yt_dlp import YoutubeDL
except Exception:
    YoutubeDL = None  # type: ignore


@dataclass
class YouTubeResult:
    title: str
    url: str
    channel: Optional[str] = None
    duration_human: Optional[str] = None


def _human_duration(seconds: Optional[int]) -> Optional[str]:
    if seconds is None:
        return None
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


class YouTubeModule(Module):
    """
    Usage:
      !youtube <query>           Search YouTube and return top result(s)
      !youtube help              Show help
      !youtube set results <n>   Set number of results (1..5)
      !youtube set cooldown <s>  Set cooldown seconds per target
    """
    MAX_RESULTS = 5

    def __init__(self, irc, *, default_results: int = 1, cooldown_s: int = 6, warn_missing: bool = True):
        # Match WeatherModule style: fantasy prefix + short command key
        # Here we keep "youtube" as the command token to align with your existing trigger.
        super().__init__(irc, "!", "youtube")
        self.results = max(1, min(int(default_results), self.MAX_RESULTS))
        self.cooldown_s = int(cooldown_s)
        self.warn_missing = warn_missing
        self._cd: Dict[str, float] = {}

    # ========== pyircsdk Module interface (WeatherModule-style) ==========

    def handleCommand(self, message, command):
        if message.command != "PRIVMSG":
            return
        if command.command != self.fantasy + self.command:
            return

        # Normalize
        frm = (message.messageFrom or "").lower()
        to = message.messageTo
        args = command.args or []

        # Help
        if len(args) == 0 or (len(args) == 1 and args[0].lower() == "help"):
            self._say(to, "Usage: !youtube <keywords> ::::: !youtube set results <1-5> ::::: !youtube set cooldown <seconds>")
            return

        # Settings subcommands
        if len(args) >= 2 and args[0].lower() == "set":
            subcmd = (args[1] if len(args) >= 2 else "").lower()
            if subcmd == "results" and len(args) >= 3:
                try:
                    n = int(args[2])
                    self.results = max(1, min(n, self.MAX_RESULTS))
                    self._say(to, f"OK {frm}: results set to {self.results}")
                except ValueError:
                    self._say(to, f"{frm}: results must be an integer 1..{self.MAX_RESULTS}")
                return
            if subcmd == "cooldown" and len(args) >= 3:
                try:
                    s = int(args[2])
                    self.cooldown_s = max(0, s)
                    self._say(to, f"OK {frm}: cooldown set to {self.cooldown_s}s")
                except ValueError:
                    self._say(to, f"{frm}: cooldown must be an integer (seconds)")
                return
            # Unknown set subcommand
            self._say(to, "Usage: !youtube set results <1-5> ::::: !youtube set cooldown <seconds>")
            return

        # Regular search
        query = " ".join(args).strip()
        if not query:
            self._say(to, f"{frm}: usage: !youtube <title or keywords>")
            return

        if self._cooldown(to):
            return

        threading.Thread(
            target=self._search_and_reply,
            args=(to, frm, query),
            daemon=True
        ).start()

    def handleError(self, message, command, error):
        # Mirror WeatherModule error handling tone
        if message.command == "PRIVMSG" and command.command == self.fantasy + self.command:
            self._say(message.messageTo, "Sorry, I was unable to handle your request. Please try again later.")
        # Optionally also log/print
        try:
            print(error)
        except Exception:
            pass

    # ========== Internal helpers ==========

    def _cooldown(self, target: str) -> bool:
        now = time.time()
        last = self._cd.get(target, 0.0)
        if now - last < self.cooldown_s:
            return True
        self._cd[target] = now
        return False

    def _search_and_reply(self, target: str, nick: str, query: str):
        if YoutubeDL is None:
            if self.warn_missing:
                self._say(target, "⚠️ yt_dlp not installed. `pip install yt-dlp`")
            return

        try:
            results = self._yt_search(query, self.results)
            if not results:
                self._say(target, f"{nick}: no results for '{query}'.")
                return

            for line in self._format(results):
                self._say(target, line)
        except Exception as e:
            self._say(target, f"{nick}: error searching YouTube: {e}")

    def _yt_search(self, query: str, limit: int) -> List[YouTubeResult]:
        opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": False,
            "noplaylist": True,
        }
        q = f"ytsearch{max(1, int(limit))}:{query}"
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(q, download=False)
        entries = (info or {}).get("entries") or []
        out: List[YouTubeResult] = []
        for e in entries[:limit]:
            out.append(
                YouTubeResult(
                    title=e.get("title") or "(no title)",
                    url=e.get("webpage_url") or e.get("url") or "",
                    channel=e.get("channel") or e.get("uploader"),
                    duration_human=_human_duration(e.get("duration")),
                )
            )
        return out

    def _format(self, results: List[YouTubeResult]) -> List[str]:
        lines: List[str] = []
        for i, r in enumerate(results, 1):
            meta = []
            if r.channel:
                meta.append(r.channel)
            if r.duration_human:
                meta.append(f"[{r.duration_human}]")
            meta_str = (" — " + " ".join(meta)) if meta else ""
            lines.append(f"🎬 {i}. {r.title}{meta_str} • {r.url}")
        return lines

    def _say(self, target: str, text: str):
        # Match WeatherModule: always use self.irc.privmsg
        try:
            self.irc.privmsg(target, text)
        except Exception:
            # Fallback to Module.privmsg if available
            try:
                self.privmsg(target, text)
            except Exception:
                pass
