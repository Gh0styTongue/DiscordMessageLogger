# Discord Message Logger

*A powerful, real-time Discord chat logger for server channels, DMs, and group chats.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)

---

## Table of Contents

- [About The Project](#about-the-project)
- [Features](#features)
- [Disclaimer](#%EF%B8%8F-disclaimer-important)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## About The Project

The Discord Message Logger is a command-line tool designed to provide a persistent, local backup of your Discord conversations. Whether you want to archive important discussions in a server, keep a personal log of your DMs, or monitor group chats, this tool offers a simple and effective solution.

It runs directly on your machine and connects to Discord using a user token, allowing it to see and log everything you have access to.

---

## Features

- **Real-time Logging**: Captures messages from server channels, direct messages (DMs), and group DMs as they happen.
- **Deleted Message Detection**: If a message is deleted in a channel you are logging, the script will mark the corresponding entry in your log file as `[DELETED]`.
- **Forwarded Message Logging**: When a message is a reply, the logger fetches the original message's author and content, providing full context.
- **User-Friendly Token Entry**: A simple GUI prompt makes it easy to enter your Discord token, which is then saved securely in a local `.env` file for future use.
- **Session Management**: Each time you restart the logger, it adds a timestamped separator to the log file, making it easy to see when a new session began.
- **Filesystem-Safe Naming**: Server and channel names are automatically sanitized to prevent issues with folder and file creation.

---

## ⚠️ Disclaimer (Important!)

This tool requires a **Discord User Token**, not a bot token. Using a user token to automate actions is against Discord's Terms of Service and can put your account at risk of being flagged or banned.

**Recommendations:**
- **Use an Alt Account**: It is strongly recommended that you **DO NOT** use your main Discord account. Create a secondary, "alt" or "throwaway" account for logging purposes.
- **Understand the Risks**: By using this tool, you acknowledge the potential risks to your Discord account. The author is not responsible for any consequences that may arise.

---

## Prerequisites

- **Python 3.6 or higher**: You can download Python from [python.org](https://www.python.org/downloads/).
- **A Discord User Token**: You will need to provide a user token from a Discord account.

---

## Installation

1.  **Clone the repository (or download the files):**
    ```bash
    git clone https://github.com/Gh0styTongue/DiscordMessageLogger
    cd DiscordMessageLogger
    ```

2.  **Install the required Python packages:**
    The script relies on `aiohttp` for asynchronous HTTP requests and `tkinter` for the token entry GUI (tkinter is usually included with Python).
    ```bash
    pip install aiohttp
    ```

---

## Usage

1.  **Run the script:**
    ```bash
    python logger.py
    ```

2.  **Enter Your Token:**
    - The first time you run the script, a GUI window will pop up asking for your Discord user token.
    - Paste your token into the field and click "Save".
    - The token will be saved to a `.env` file in the same directory, so you won't have to enter it again unless it becomes invalid.
    - If the token is ever invalid, the script will automatically prompt you to enter a new one.

3.  **Select Logging Mode:**
    - In your terminal, you will be asked to choose between logging **Server Channels** or **DMs**.
    ```
    1) Server channels
    2) DMs
    Select:
    ```

4.  **Select Your Target:**
    - **If you chose Servers:** You will be presented with a numbered list of servers your account is in. Enter the number corresponding to your desired server. Then, you will see a list of channels in that server. Enter the number for the channel you wish to log.
    - **If you chose DMs:** You will see a numbered list of your recent DMs and group chats. Enter the number for the conversation you want to log.

5.  **Start Logging:**
    - The script will immediately begin logging messages in the selected channel or DM. New messages will be printed to the console and saved to a log file.
    - To stop the logger, press `Ctrl+C` in your terminal.

---

## File Structure

The script will create folders and files to store the logs, organized as follows:

```
Server_Name/
└── live_ChannelName.txt       # Log file for a server channel

DMs/
└── live_Username_or_GroupName.txt # Log file for a DM or group chat
```

- `Server_Name` and `ChannelName` (or `Username`) are sanitized versions of the actual names on Discord.

---

## How It Works

The `DiscordLogger` class manages the entire logging process. Here's a high-level overview:
- It uses the `aiohttp` library to make asynchronous GET requests to the Discord API endpoints.
- After a valid token is provided, it fetches the user's guilds (servers) and DM channels.
- Once a target channel is selected, it enters an asynchronous loop (`log_loop`).
- In each iteration, it fetches the last 50 messages from the channel.
- It compares the new message IDs with the IDs it has already logged to identify new messages.
- It also checks if any previously seen messages are now missing, which indicates they were deleted.
- New messages are formatted and appended to the appropriate log file and printed to the console.
- The loop runs with a short delay to avoid hitting API rate limits.

---

## Contributing

Contributions are welcome! If you have a suggestion or find a bug, please open an issue to discuss it.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Acknowledgments

- Copyright (c) 2024 GhostyTongue (Original Author)
- This README was generated and enhanced by an AI assistant.
