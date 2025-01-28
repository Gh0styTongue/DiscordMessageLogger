import asyncio
import aiohttp
import os
import re
import signal
import sys

BASE_URL = "https://discord.com/api/v9"
TOKEN = "TOKEN_HERE"
HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}

selected_server = None
selected_channel = None
selected_channel_id = None
logging_active = True
logged_messages = {}
last_message_id = None
download_attachments = False

async def fetch_data(session, url):
    async with session.get(url, headers=HEADERS) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"API Error: {url} returned status code {response.status}")
            return None

async def get_current_user(session):
    url = f"{BASE_URL}/users/@me"
    return await fetch_data(session, url)

async def download_attachment(attachment_url, server_name, channel_name, filename):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(attachment_url) as response:
                if response.status == 200:
                    attachment_folder = os.path.join(server_name, channel_name, "attachments")
                    if not os.path.exists(attachment_folder):
                        os.makedirs(attachment_folder)
                    
                    file_path = os.path.join(attachment_folder, filename)
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                    print(f"Downloaded: {file_path}")
        except Exception as e:
            print(f"Failed to download attachment: {e}")

async def get_user_guilds(session):
    url = f"{BASE_URL}/users/@me/guilds"
    guilds = await fetch_data(session, url)
    return guilds if guilds else []

async def get_guild_channels(session, guild_id):
    url = f"{BASE_URL}/guilds/{guild_id}/channels"
    channels = await fetch_data(session, url)
    return [ch for ch in channels if ch and ch.get('type') == 0] if channels else []

async def get_dm_channels(session):
    url = f"{BASE_URL}/users/@me/channels"
    channels = await fetch_data(session, url)
    return [ch for ch in channels if ch and ch.get('type') in (1, 3)] if channels else []

async def fetch_messages(session, channel_id, limit=50):
    url = f"{BASE_URL}/channels/{channel_id}/messages?limit={limit}"
    return await fetch_data(session, url)

def clean_name(name):
    try:
        cleaned = re.sub(r'[^\w\s-]', '', name)
        cleaned = re.sub(r'[\s-]+', '_', cleaned)
        return cleaned if cleaned else "default"
    except Exception:
        return "default"

async def log_messages_from_current(channel_id, channel_name, server_name):
    global logged_messages, last_message_id
    logged_messages = {}

    server_clean = clean_name(server_name)
    channel_clean = clean_name(channel_name)

    try:
        os.makedirs(server_clean, exist_ok=True)
    except OSError:
        server_clean = "fallback_server"

    log_file_path = os.path.join(server_clean, f"live_{channel_clean}.txt")

    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            while logging_active:
                try:
                    async with aiohttp.ClientSession() as session:
                        messages = await fetch_messages(session, channel_id)
                        if messages:
                            for message in messages:
                                if message['id'] not in logged_messages:
                                    date = message['timestamp'].split('T')[0]
                                    time = message['timestamp'].split('T')[1].split('.')[0]
                                    log_entry = f"[ID: {message['id']}] On {date} at {time}, {message['author']['username']} said: {message['content']}\n"
                                    
                                    embeds = message.get('embeds', [])
                                    attachments = message.get('attachments', [])
                                    stickers = message.get('sticker_items', [])
                                    reference = message.get('referenced_message', None)
                                    
                                    for embed in embeds:
                                        if 'url' in embed:
                                            log_entry += f"Embed URL: {embed['url']}\n"
                                        elif 'title' in embed and 'description' in embed:
                                            log_entry += f"Embed: {embed['title']} - {embed['description']}\n"
                                    
                                    for attachment in attachments:
                                        log_entry += f"Attachment URL: {attachment['url']}\n"
                                        if download_attachments:
                                            await download_attachment(attachment['url'], server_clean, channel_clean, attachment['filename'])

                                    for sticker in stickers:
                                        log_entry += f"Sticker: {sticker['name']} (ID: {sticker['id']})\n"

                                    if reference:
                                        log_entry += f"Reply to: {reference['author']['username']} - {reference['content'][:50]}...\n"

                                    if 'flags' in message and message['flags'] & 1 << 11: 
                                        log_entry += f"Forwarded from: {message.get('referenced_message', {}).get('id', 'Unknown')}\n"

                                    try:
                                        log_file.write(log_entry)
                                        log_file.flush()
                                        logged_messages[message['id']] = log_entry
                                        print(log_entry.strip())
                                    except IOError:
                                        print(f"Failed to write to log file.")
                                    last_message_id = message['id']

                        print(f"Logged Messages: {len(logged_messages)}")
                
                except Exception as e:
                    print(f"Error in logging loop: {e}")

                await asyncio.sleep(0.5)

    except Exception as e:
        print(f"Major error in logging process: {e}")

async def select_server(max_retries=3):
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                guilds = await get_user_guilds(session)
                if not guilds:
                    print(f"Retry {attempt + 1}/{max_retries}: No servers available.")
                    continue
                print("Available servers:")
                for idx, guild in enumerate(guilds, 1):
                    print(f"{idx}: {guild['name']}")
                
                while True:
                    try:
                        choice = int(input("\nSelect a server by number: ")) - 1
                        if 0 <= choice < len(guilds):
                            global selected_server
                            selected_server = guilds[choice]['name']
                            return selected_server
                        else:
                            print("Invalid choice. Try again.")
                    except ValueError:
                        print("Please enter a number.")
        except Exception as e:
            print(f"Error selecting server (Attempt {attempt + 1}): {e}")
    print("Failed to select a server after multiple attempts.")
    return None

async def select_channel(max_retries=3):
    for attempt in range(max_retries):
        try:
            if not selected_server:
                print("No server selected. Please select a server first.")
                return None
            
            async with aiohttp.ClientSession() as session:
                guilds = await get_user_guilds(session)
                guild_id = next((g['id'] for g in guilds if g['name'] == selected_server), None)
                if guild_id is None:
                    print(f"Retry {attempt + 1}/{max_retries}: Server name not found in guild list.")
                    continue
                channels = await get_guild_channels(session, guild_id)
                if not channels:
                    print(f"Retry {attempt + 1}/{max_retries}: No channels available in this server.")
                    continue
                print(f"\nAvailable channels for '{selected_server}':")
                for idx, channel in enumerate(channels, 1):
                    print(f"{idx}: {channel['name']} (ID: {channel['id']})")

                while True:
                    try:
                        choice = int(input("\nSelect a channel by number: ")) - 1
                        if 0 <= choice < len(channels):
                            global selected_channel, selected_channel_id
                            selected_channel = channels[choice]['name']
                            selected_channel_id = channels[choice]['id']
                            return selected_channel
                        else:
                            print("Invalid choice. Try again.")
                    except ValueError:
                        print("Please enter a number.")
        except Exception as e:
            print(f"Error selecting channel (Attempt {attempt + 1}): {e}")
    print("Failed to select a channel after multiple attempts.")
    return None

async def select_dm_channel(max_retries=3):
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                dm_channels = await get_dm_channels(session)
                if not dm_channels:
                    print(f"Retry {attempt + 1}/{max_retries}: No DM channels available.")
                    continue
                
                channels_with_display = []
                for ch in dm_channels:
                    if ch['type'] == 1:
                        recipients = ch.get('recipients', [])
                        names = [r['username'] for r in recipients] if recipients else []
                        display = ', '.join(names) if names else f"DM-{ch['id']}"
                    else:
                        display = ch.get('name', 'Unnamed Group DM')
                        if not display:
                            recipients = ch.get('recipients', [])
                            names = [r['username'] for r in recipients] if recipients else []
                            display = ', '.join(names) if names else 'Empty Group DM'
                    channels_with_display.append((ch, display))

                print("Available DM channels:")
                for idx, (ch, disp) in enumerate(channels_with_display, 1):
                    print(f"{idx}: {disp} (ID: {ch['id']})")

                while True:
                    try:
                        choice = int(input("\nSelect a DM channel by number: ")) - 1
                        if 0 <= choice < len(channels_with_display):
                            global selected_server, selected_channel, selected_channel_id
                            selected_ch, display_name = channels_with_display[choice]
                            selected_server = "DMs"
                            selected_channel = display_name
                            selected_channel_id = selected_ch['id']
                            return selected_channel
                        else:
                            print("Invalid choice. Try again.")
                    except ValueError:
                        print("Please enter a number.")
        except Exception as e:
            print(f"Error selecting DM channel (Attempt {attempt + 1}): {e}")
    print("Failed to select a DM channel after multiple attempts.")
    return None

async def start_logging():
    global selected_channel, selected_server
    try:
        if not selected_channel:
            print("No channel selected. Please select a channel first.")
            return
        
        print(f"Starting logging for channel '{selected_channel}'...")
        server_name = selected_server if selected_server else "DMs"
        await log_messages_from_current(selected_channel_id, selected_channel, server_name)
    except Exception as e:
        print(f"Logging failed to start: {e}")

def stop_logging():
    global logging_active
    logging_active = False
    print("Logging stopped.")
    print(f"Final count - Logged Messages: {len(logged_messages)}")

def handle_exit(signum, frame):
    print("\nReceived exit signal. Stopping logging...")
    stop_logging()
    asyncio.get_event_loop().stop()

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            user = await get_current_user(session)
            if user:
                print(f"Logged into account: {user.get('username', 'Unknown')}")
            else:
                print("Could not fetch user information.")

            global download_attachments
            download_attachments = input("Would you like to download attachments? (yes/no): ").lower() == 'yes'

            print("\nChoose where to log messages:")
            print("1: Server channels")
            print("2: Direct Messages (DMs)")
            choice = input("Enter 1 or 2: ").strip()

            if choice == '1':
                print("\nFetching servers...")
                await select_server()
                await select_channel()
            elif choice == '2':
                print("\nFetching DMs...")
                await select_dm_channel()
            else:
                print("Invalid choice. Exiting.")
                return

            await start_logging()
    except Exception as e:
        print(f"An error occurred in main process: {e}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    asyncio.run(main())
