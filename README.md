# Discord Message Logger

**Warning: This script logs messages in real-time from Discord servers and channels, including deleted messages. It is important to follow Discord's Terms of Service (ToS) and use this script responsibly.**

This script is designed to log messages from a selected Discord server and channel, including deleted messages. It can be used with both **Discord bot tokens** and **Discord user tokens**. The logged messages are saved to a file on your local machine. This script can be useful for archiving, monitoring, or auditing Discord chats, but **must only be used in compliance with Discord's Terms of Service (ToS)**.

## Important Legal Disclaimer

By using this script, **you agree to comply with Discord's Terms of Service (ToS)**, which prohibit unauthorized data scraping, spamming, and violating user privacy. **Misuse of this script may result in account bans or legal action from Discord.**

- **Discord ToS:** https://discord.com/terms

### Key Points:
- **Bot Tokens vs. User Tokens:**
   - **Bot Tokens**: Used for bots that have permissions granted by the server administrators. Bots are limited by the permissions assigned and cannot log private or direct messages unless explicitly allowed.
   - **User Tokens**: Can be used for actions that mimic a user’s behavior, giving more direct access to server messages and interactions. **Using user tokens for logging is risky and can violate Discord's ToS**, especially if you do not have consent from server members.

- **Logging of Deleted Messages:** This script logs not only messages as they are posted but also deleted messages if the bot has appropriate permissions. Be aware that logging deleted messages may violate privacy and community guidelines.
- **Usage with Bad Intentions:** While this script can be used for legitimate purposes like archiving public conversations, **it can also be misused for malicious activities**, including spying on users or collecting private information without consent. We strongly advise against using this script for any illegal or harmful purposes.

## Requirements

- Python 3.7 or later
- `aiohttp` library for asynchronous HTTP requests

You can install the required dependencies using `pip`:

```bash
pip install aiohttp
```

## How to Use

1. **Set up your Discord bot or user token:**
   - Replace the `TOKEN` variable in the script with your Discord **bot token** or **user token**. 
     - **Bot Token:** If you're using a bot, make sure the bot has permissions to access and log messages from the selected channels.
     - **User Token:** If you're using a user token (which is against Discord's ToS for automated access), be aware that this is a violation of Discord's guidelines, and **it can result in account bans**. We strongly advise against using user tokens for logging purposes.

2. **Running the Script:**
   - Run the script with Python.

   ```bash
   python logger.py
   ```

3. **Selecting a Server and Channel:**
   - The script will prompt you to select a server and then a channel within that server.
   - It will display a list of available servers and channels. Enter the number corresponding to your selection.

4. **Logging:**
   - Once a channel is selected, the script will start logging messages in real-time, including deleted messages, if the bot has the appropriate permissions.
   - Messages will be saved in a text file within a directory named after the server.
   - The format of the log is: `[ID: <message_id>] On <date> at <time>, <username> said: <message_content>`.

5. **Stopping the Logging:**
   - To stop logging, simply terminate the script (e.g., press `Ctrl+C`).
   - The script will print the total number of logged messages and stop.

## Key Functions

- `fetch_data(session, url)`: Fetches data from a given API endpoint.
- `get_user_guilds(session)`: Retrieves a list of guilds (servers) the bot is part of.
- `get_guild_channels(session, guild_id)`: Fetches the channels of a specific guild.
- `fetch_messages(session, channel_id, limit=50)`: Retrieves messages from a specific channel.
- `log_messages_from_current(channel_id, channel_name, server_name)`: Logs messages from a selected channel and server.
- `clean_server_name(server_name)`: Sanitizes the server name to be used as a directory name.
- `select_server()`: Prompts the user to select a server from the available list.
- `select_channel()`: Prompts the user to select a channel from the selected server.
- `start_logging()`: Begins logging messages to a file.
- `stop_logging()`: Stops the logging process.
- `handle_exit()`: Gracefully handles exit signals to stop logging.

## Notes

- **Logging of Deleted Messages:** This script logs deleted messages, which can be a violation of user privacy. Be aware of how you use this script to avoid violating Discord's ToS.
- The script only logs messages from text channels (channel type 0).
- The logging process continues indefinitely, refreshing messages every 0.5 seconds.
- If a channel has a lot of messages, consider adjusting the `limit` argument in the `fetch_messages` function.

## Ethical Usage

Before using this script, please ensure that you have permission from the server administrators and members to log messages. Using this script without consent may result in negative consequences, including the termination of your Discord account. **It is important to note that using user tokens for this purpose is against Discord’s ToS**, and can result in your account being banned. Always act responsibly and in accordance with Discord’s guidelines and community rules.

## License

This script is provided under the MIT License. Feel free to use and modify it as needed, but always respect the privacy and consent of others in Discord servers.

## Conclusion

While this script can serve legitimate purposes such as archiving or monitoring public channels, **it is essential to be aware of how it can be misused**. Unauthorized use of this script may violate Discord’s Terms of Service, result in account bans, and have legal repercussions. Use responsibly, and always follow Discord’s guidelines and ToS.

### Key Changes:
1. **Bot vs. User Token Clarification:** I've added explicit mentions that the script can work with both bot and user tokens, but using a user token violates Discord’s ToS and can lead to account bans.
2. **Updated Warnings on User Token Use:** Emphasized that using user tokens for this script is risky and against Discord's guidelines.
3. **Legal and Ethical Warnings:** Expanded the legal and ethical usage section to reflect concerns about both token types, particularly with respect to deleted messages.
