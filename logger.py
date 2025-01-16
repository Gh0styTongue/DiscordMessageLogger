import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import aiohttp
import os
import json

BASE_URL = "https://discord.com/api/v9"
TOKEN = "Token_Here"
HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}

class DiscordLoggerApp:
    def __init__(self, root, loop):
        self.root = root
        self.loop = loop
        self.root.title("Discord Logger")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C2F33")

        self.session = None
        self.selected_server = None
        self.selected_channels = []
        self.logging_active = False
        self.logged_messages = {}
        self.download_attachments = tk.BooleanVar()
        self.log_dir = os.path.join(os.getcwd(), "logs")

        self.create_widgets()

    def create_widgets(self):
        self.frame_left = tk.Frame(self.root, bg="#23272A", width=200)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y)

        self.label_servers = tk.Label(self.frame_left, text="Servers", bg="#23272A", fg="#FFFFFF", font=("Arial", 12))
        self.label_servers.pack(pady=10)
        self.list_servers = tk.Listbox(self.frame_left, bg="#2C2F33", fg="#FFFFFF", font=("Arial", 10), selectbackground="#7289DA")
        self.list_servers.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.list_servers.bind("<<ListboxSelect>>", self.on_server_selected)

        self.frame_right = tk.Frame(self.root, bg="#2C2F33")
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.label_channels = tk.Label(self.frame_right, text="Channels", bg="#2C2F33", fg="#FFFFFF", font=("Arial", 12))
        self.label_channels.pack(pady=10)
        self.list_channels = tk.Listbox(self.frame_right, bg="#2C2F33", fg="#FFFFFF", font=("Arial", 10), selectbackground="#7289DA", selectmode=tk.MULTIPLE)
        self.list_channels.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.list_channels.bind("<<ListboxSelect>>", self.on_channel_selected)

        self.checkbox_attachments = tk.Checkbutton(self.frame_right, text="Download Attachments", variable=self.download_attachments, bg="#2C2F33", fg="#FFFFFF", selectcolor="#23272A", font=("Arial", 10))
        self.checkbox_attachments.pack(pady=10)

        self.btn_start_logging = ttk.Button(self.frame_right, text="Start Logging", command=self.start_logging)
        self.btn_start_logging.pack(pady=5)
        self.btn_stop_logging = ttk.Button(self.frame_right, text="Stop Logging", command=self.stop_logging, state=tk.DISABLED)
        self.btn_stop_logging.pack(pady=5)

        self.label_status = tk.Label(self.frame_right, text="Status: Not logged in", bg="#2C2F33", fg="#FFFFFF", font=("Arial", 10))
        self.label_status.pack(pady=10)

        self.btn_clear_logs = ttk.Button(self.frame_right, text="Clear Logs", command=self.clear_logs)
        self.btn_clear_logs.pack(pady=5)

    async def fetch_data(self, url):
        async with self.session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                return await response.json()
            else:
                messagebox.showerror("API Error", f"Failed to fetch data from {url}. Status: {response.status}")
                return None

    async def load_servers(self):
        url = f"{BASE_URL}/users/@me/guilds"
        guilds = await self.fetch_data(url)
        if guilds:
            self.list_servers.delete(0, tk.END)
            for guild in guilds:
                self.list_servers.insert(tk.END, guild['name'])

    async def load_channels(self):
        selected_server_name = self.list_servers.get(tk.ACTIVE)
        url = f"{BASE_URL}/users/@me/guilds"
        guilds = await self.fetch_data(url)
        guild_id = next((g['id'] for g in guilds if g['name'] == selected_server_name), None)
        if guild_id:
            url = f"{BASE_URL}/guilds/{guild_id}/channels"
            channels = await self.fetch_data(url)
            self.list_channels.delete(0, tk.END)
            for channel in channels:
                if channel['type'] == 0:  # Text channels only
                    self.list_channels.insert(tk.END, f"{channel['name']} (ID: {channel['id']})")

    async def log_messages(self):
        if not self.selected_channels:
            return
        self.logging_active = True
        self.btn_start_logging["state"] = tk.DISABLED
        self.btn_stop_logging["state"] = tk.NORMAL
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        while self.logging_active:
            for channel_id in self.selected_channels:
                url = f"{BASE_URL}/channels/{channel_id}/messages?limit=50"
                messages = await self.fetch_data(url)
                if messages:
                    for message in messages:
                        if message['id'] not in self.logged_messages:
                            self.logged_messages[message['id']] = message
                            log_file = os.path.join(self.log_dir, f"{channel_id}.json")
                            with open(log_file, 'a+') as f:
                                f.write(json.dumps(message) + '\n')
                            print(f"{message['author']['username']}: {message['content']}")
                            if self.download_attachments.get() and 'attachments' in message and message['attachments']:
                                await self.download_attachments_files(message['attachments'], channel_id)
            await asyncio.sleep(0.1)
        self.btn_start_logging["state"] = tk.NORMAL
        self.btn_stop_logging["state"] = tk.DISABLED

    async def download_attachments_files(self, attachments, channel_id):
        for attachment in attachments:
            filename = os.path.join(self.log_dir, f"{channel_id}_{attachment['id']}_{attachment['filename']}")
            async with self.session.get(attachment['url']) as resp:
                if resp.status == 200:
                    with open(filename, 'wb') as out_file:
                        out_file.write(await resp.read())

    def start_logging(self):
        if not self.selected_server or not self.selected_channels:
            messagebox.showwarning("Warning", "Please select a server and at least one channel before starting logging.")
            return
        if len(self.selected_channels) > 3:
            messagebox.showwarning("Warning", "Warning: Logging more than 3 channels may cause instability, high local resource usage, and potential Discord account issues. Use caution.")
        self.loop.create_task(self.log_messages())

    def stop_logging(self):
        self.logging_active = False
        messagebox.showinfo("Info", "Logging stopped.")

    def on_server_selected(self, event):
        self.selected_server = self.list_servers.get(tk.ACTIVE)
        self.loop.create_task(self.load_channels())

    def on_channel_selected(self, event):
        selected_channel_indices = self.list_channels.curselection()
        self.selected_channels = []
        for idx in selected_channel_indices:
            selected_channel_text = self.list_channels.get(idx)
            channel_id = selected_channel_text.split(" (ID: ")[1].rstrip(")")
            self.selected_channels.append(channel_id)

    async def main(self):
        self.session = aiohttp.ClientSession()
        url = f"{BASE_URL}/users/@me"
        user = await self.fetch_data(url)
        if user:
            self.label_status.config(text=f"Logged in as: {user.get('username', 'Unknown')}")
            await self.load_servers()
        else:
            messagebox.showerror("Error", "Failed to log in.")

    def on_close(self):
        self.loop.run_until_complete(self.session.close())
        self.root.destroy()

    def clear_logs(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all logs?"):
            for file in os.listdir(self.log_dir):
                os.remove(os.path.join(self.log_dir, file))
            messagebox.showinfo("Success", "All logs have been cleared.")

def run_app():
    root = tk.Tk()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = DiscordLoggerApp(root, loop)

    def update_loop():
        loop.call_soon(loop.stop)
        loop.run_forever()
        root.after(100, update_loop)

    root.after(100, update_loop)
    loop.run_until_complete(app.main())
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    run_app()
