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

async def get_user_guilds(session):
    url = f"{BASE_URL}/users/@me/guilds"
    guilds = await fetch_data(session, url)
    return guilds if guilds else []

async def get_guild_channels(session, guild_id):
    url = f"{BASE_URL}/guilds/{guild_id}/channels"
    channels = await fetch_data(session, url)
    return [ch for ch in channels if ch and ch.get('type') == 0] if channels else []

async def fetch_messages(session, channel_id, limit=1):
    url = f"{BASE_URL}/channels/{channel_id}/messages?limit={limit}"
    return await fetch_data(session, url)

async def log_messages_from_current(channel_id, channel_name, server_name):
    global logged_messages, last_message_id
    logged_messages = {}

    try:
        os.makedirs(server_name, exist_ok=True)
    except OSError:
        server_name = "fallback_server"

    log_file_path = os.path.join(server_name, f"live_{channel_name}.txt")

    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            while logging_active:
                try:
                    async with aiohttp.ClientSession() as session:
                        messages = await fetch_messages(session, channel_id)
                        if messages:
                            latest_message = messages[0]

                            for message in messages:
                                if message['id'] not in logged_messages:
                                    date = message['timestamp'].split('T')[0]
                                    time = message['timestamp'].split('T')[1].split('.')[0]
                                    log_entry = f"[ID: {message['id']}] On {date} at {time}, {message['author']['username']} said: {message['content']}\n"
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

def clean_server_name(server_name):
    try:
        cleaned_name = re.sub(r'[^\w\s-]', '', server_name)
        cleaned_name = re.sub(r'[\s-]+', '_', cleaned_name)
        return cleaned_name if cleaned_name else "default_server"
    except Exception:
        return "default_server"

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

async def start_logging():
    global selected_channel, selected_server
    try:
        if not selected_channel:
            print("No channel selected. Please select a channel first.")
            return
        
        if not selected_server:
            print("No server selected. Please select a server first.")
            return
        
        print(f"Starting logging for channel '{selected_channel}' on server '{selected_server}'...")
        await log_messages_from_current(selected_channel_id, selected_channel, clean_server_name(selected_server))
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

        print("Fetching available servers...")
        await select_server()
        await select_channel()
        await start_logging()
    except Exception as e:
        print(f"An error occurred in main process: {e}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)  
    signal.signal(signal.SIGTERM, handle_exit)  
    asyncio.run(main())
