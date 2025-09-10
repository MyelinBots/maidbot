from __future__ import annotations
import re, time, threading
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
    if seconds is None: return None
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

class YouTubeModule(Module):
    CMD = re.compile(r"^!youtube\s+(.+)$", re.I)

    def __init__(self, irc, *, results: int = 1, cooldown_s: int = 6, warn_missing: bool = True):
        super().__init__(irc)
        self.results = max(1, int(results))
        self.cooldown_s = int(cooldown_s)
        self.warn_missing = warn_missing
        self._cd: Dict[str, float] = {}

    def startListening(self):
        # try multiple pyircsdk variants
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
            self._say(target, f"{nick}: usage: !youtube <title or keywords>")
            return
        if self._cooldown(target): return
        threading.Thread(target=self._search_and_reply, args=(target, nick, query), daemon=True).start()

    def _cooldown(self, target: str) -> bool:
        now = time.time(); last = self._cd.get(target, 0)
        if now - last < self.cooldown_s: return True
        self._cd[target] = now; return False

    def _search_and_reply(self, target: str, nick: str, query: str):
        if YoutubeDL is None:
            if self.warn_missing:
                self._say(target, "⚠️ yt_dlp not installed. `pip install yt-dlp`")
            return
        try:
            results = self._yt_search(query, self.results)
            if not results:
                self._say(target, f"{nick}: no results for '{query}'."); return
            for line in self._format(results):
                self._say(target, line)
        except Exception as e:
            self._say(target, f"{nick}: error searching YouTube: {e}")

    def _yt_search(self, query: str, limit: int) -> List[YouTubeResult]:
        opts = {"quiet": True, "skip_download": True, "extract_flat": False, "noplaylist": True}
        q = f"ytsearch{max(1, int(limit))}:{query}"
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(q, download=False)
        entries = info.get("entries") or []
        out: List[YouTubeResult] = []
        for e in entries[:limit]:
            out.append(YouTubeResult(
                title=e.get("title") or "(no title)",
                url=e.get("webpage_url") or e.get("url") or "",
                channel=e.get("channel") or e.get("uploader"),
                duration_human=_human_duration(e.get("duration")),
            ))
        return out

    def _format(self, results: List[YouTubeResult]) -> List[str]:
        lines = []
        for i, r in enumerate(results, 1):
            meta = []
            if r.channel: meta.append(r.channel)
            if r.duration_human: meta.append(f"[{r.duration_human}]")
            meta_str = (" — " + " ".join(meta)) if meta else ""
            lines.append(f"🎬 {i}. {r.title}{meta_str} • {r.url}")
        return lines

    def _say(self, target: str, text: str):
        try: self.privmsg(target, text)
        except AttributeError: self.irc.privmsg(target, text)
