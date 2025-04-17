import asyncio
import aiohttp
import os
import re
import signal
import sys
import logging
import tkinter as tk
from datetime import datetime
from typing import Optional, Dict, List, Set

BASE_URL = "https://discord.com/api/v9"
ENV_FILE = ".env"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("discord-logger")

def load_token() -> Optional[str]:
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("DISCORD_TOKEN="):
                    return line.strip().split("=", 1)[1]
    return None

def save_token(token: str) -> None:
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(f"DISCORD_TOKEN={token}")

def prompt_token() -> str:
    root = tk.Tk()
    root.title("Enter Discord Token")
    var = tk.StringVar()
    tk.Entry(root, textvariable=var, width=50).pack(padx=10, pady=10)
    tk.Button(root, text="Save", command=root.destroy).pack(pady=(0,10))
    root.mainloop()
    return var.get().strip()

class DiscordLogger:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.server: Optional[str] = None
        self.server_id: Optional[str] = None
        self.channel: Optional[str] = None
        self.channel_id: Optional[str] = None
        self.logged_messages: Dict[str, str] = {}
        self.previous_window_ids: Set[str] = set()
        self.deleted_ids: Set[str] = set()
        self.active: bool = True

    async def fetch_json(self, url: str) -> Optional[List[Dict]]:
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                logger.error(f"{url} returned {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error {e} for {url}")
        return None

    async def fetch_message(self, channel_id: str, message_id: str) -> Optional[Dict]:
        url = f"{BASE_URL}/channels/{channel_id}/messages/{message_id}"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
        except aiohttp.ClientError:
            pass
        return None

    async def get_current_user(self) -> Optional[Dict]:
        return await self.fetch_json(f"{BASE_URL}/users/@me")

    async def get_user_guilds(self) -> List[Dict]:
        return await self.fetch_json(f"{BASE_URL}/users/@me/guilds") or []

    async def get_guild_channels(self, guild_id: str) -> List[Dict]:
        data = await self.fetch_json(f"{BASE_URL}/guilds/{guild_id}/channels") or []
        return [ch for ch in data if ch.get("type") == 0]

    async def get_dm_channels(self) -> List[Dict]:
        data = await self.fetch_json(f"{BASE_URL}/users/@me/channels") or []
        return [ch for ch in data if ch.get("type") in (1, 3)]

    def clean_name(self, name: str) -> str:
        s = re.sub(r"[^\w\s-]", "", name)
        return re.sub(r"[\s-]+", "_", s) or "default"

    async def select_server(self):
        guilds = await self.get_user_guilds()
        for i, g in enumerate(guilds, 1):
            print(f"{i}: {g['name']}")
        idx = int(input("Select server: ")) - 1
        self.server = guilds[idx]["name"]
        self.server_id = guilds[idx]["id"]

    async def select_channel(self):
        channels = await self.get_guild_channels(self.server_id)
        for i, ch in enumerate(channels, 1):
            print(f"{i}: {ch['name']} (ID: {ch['id']})")
        idx = int(input("Select channel: ")) - 1
        self.channel = channels[idx]["name"]
        self.channel_id = channels[idx]["id"]

    async def select_dm(self):
        dms = await self.get_dm_channels()
        for i, ch in enumerate(dms, 1):
            name = ch.get("name") or ", ".join(r["username"] for r in ch.get("recipients", []))
            print(f"{i}: {name} (ID: {ch['id']})")
        idx = int(input("Select DM: ")) - 1
        chosen = dms[idx]
        self.server = "DMs"
        self.channel = chosen.get("name") or ", ".join(r["username"] for r in chosen.get("recipients", []))
        self.channel_id = chosen["id"]

    async def log_loop(self):
        server_dir = self.clean_name(self.server or "DMs")
        channel_dir = self.clean_name(self.channel or "unknown")
        os.makedirs(server_dir, exist_ok=True)
        log_path = os.path.join(server_dir, f"live_{channel_dir}.txt")

        if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
            sep = datetime.now().strftime("--- %Y-%m-%d %H:%M:%S ---\n")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write("\n" + sep)

        with open(log_path, "a", encoding="utf-8") as log_file:
            while self.active:
                url = f"{BASE_URL}/channels/{self.channel_id}/messages?limit=50"
                msgs = await self.fetch_json(url) or []
                current_ids = {m["id"] for m in msgs}

                if self.previous_window_ids:
                    for mid in self.previous_window_ids:
                        if mid not in current_ids and mid not in self.deleted_ids:
                            logger.warning(f"Deleted message caught before deletion. See {log_path}")
                            with open(log_path, "r+", encoding="utf-8") as f:
                                data = f.read()
                                entry = self.logged_messages.get(mid, "").rstrip("\n")
                                updated = data.replace(entry, f"{entry} [DELETED]")
                                f.seek(0)
                                f.write(updated)
                                f.truncate()
                            self.deleted_ids.add(mid)

                self.previous_window_ids = current_ids

                for m in reversed(msgs):
                    mid = m["id"]
                    if mid not in self.logged_messages:
                        ts = m["timestamp"]
                        date, time = ts.split("T")[0], ts.split("T")[1].split(".")[0]
                        author = m["author"]["username"]
                        content = m["content"]
                        entry = f"[ID: {mid}] On {date} at {time}, {author} said: {content}\n"

                        ref = m.get("message_reference", {})
                        ref_id = ref.get("message_id")
                        if ref_id:
                            orig = await self.fetch_message(self.channel_id, ref_id)
                            if orig:
                                orig_author = orig["author"]["username"]
                                orig_content = orig["content"]
                                entry += f"Forwarded from {orig_author} said: {orig_content}\n"
                            else:
                                entry += f"Forwarded from msg ID: {ref_id} [DELETED]\n"

                        log_file.write(entry)
                        log_file.flush()
                        self.logged_messages[mid] = entry
                        print(entry.strip())

                logger.info(f"Total logged: {len(self.logged_messages)}")
                await asyncio.sleep(0.5)

    def stop(self):
        self.active = False
        logger.info(f"Stopped. Total messages logged: {len(self.logged_messages)}")

    async def run(self):
        while True:
            token = load_token() or prompt_token()
            save_token(token)
            headers = {"Authorization": token, "Content-Type": "application/json"}
            async with aiohttp.ClientSession(headers=headers) as sess:
                self.session = sess
                user = await self.get_current_user()
                if not user:
                    logger.error("Invalid token, please re-enter")
                    continue
                logger.info(f"Logged in as {user.get('username')}")
                mode = input("1) Server channels\n2) DMs\nSelect: ").strip()
                if mode == "1":
                    await self.select_server()
                    await self.select_channel()
                elif mode == "2":
                    await self.select_dm()
                else:
                    logger.error("Invalid selection")
                    return
                await self.log_loop()
                break

def main():
    dl = DiscordLogger()
    signal.signal(signal.SIGINT, lambda s, f: dl.stop())
    signal.signal(signal.SIGTERM, lambda s, f: dl.stop())
    asyncio.run(dl.run())

if __name__ == "__main__":
    main()
