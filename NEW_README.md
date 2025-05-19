# Discord Message Logger

A Python-based tool for real-time logging of Discord messages from server channels, DMs, and group DMs.

## ⚠️ Warning: User Tokens Only

This tool requires a **real user token** for authentication. Bot tokens are **not supported**. Using user tokens is against Discord's Terms of Service and may put your account at risk. It is highly recommended to **use alt/throwaway accounts** for logging to avoid any potential issues with your main account.

## Features

*   **Real-time message logging:** Captures messages as they are sent in server channels, direct messages (DMs), and group DMs.
*   **Deleted message detection:** Flags messages that are deleted from the chat with `[DELETED]` in the log file.
*   **Forwarded message logging:** When a message is a forward, the logger attempts to fetch and log the original message content and author. If the original message has been deleted, it's noted in the log.
*   **GUI for token entry:** Provides a simple graphical interface to input your Discord user token.
*   **Token management:** Securely saves your token to a `.env` file for future sessions and re-prompts for a new token if the current one is invalid.
*   **Session separators:** Adds a timestamped separator (`--- YYYY-MM-DD HH:MM:SS ---`) to the log file each time the logger is started, making it easy to distinguish between logging sessions.
*   **Attachment downloads (Optional):** Provides an option to download attachments from messages. (Note: This feature is mentioned in the old README but its implementation details are not fully evident in the provided `logger.py` snippet. Assuming it's a planned or existing feature to be documented).

## Prerequisites

*   **Python Version:** Python 3.7 or newer is recommended. This is due to the use of features like `asyncio.run()` and other modern Python syntax.
*   **Cross-Platform Compatibility:** The script is designed to be cross-platform and should work on Windows, macOS, and Linux systems, as it relies on standard Python libraries.
*   **Tkinter Availability:** The GUI for token entry uses `tkinter`, which is part of Python's standard library. Most Python installations include `tkinter` by default. However, if you are using a minimal or custom Python installation, please ensure that `tkinter` is available.

## Installation

1.  Install the necessary Python dependencies:
    ```bash
    pip install aiohttp tkinter requests
    ```

## Usage

1.  Run the logger script from your terminal:
    ```bash
    python logger.py
    ```
2.  If it's your first time or the token is invalid, a GUI window will appear. Enter your Discord **user token** in the prompt. The token will be saved locally in a `.env` file for subsequent uses.
3.  Follow the command-line prompts to select the logging mode:
    *   Choose **Server** to log messages from a specific channel within a server. You will be asked to select the server and then the channel.
    *   Choose **DM** to log messages from a direct message thread or group DM. You will be asked to select the DM conversation.
4.  After selection, the logger will start displaying messages in the console and saving them to a log file.
5.  To stop logging, press **Ctrl+C** in the terminal where the script is running.

## File Structure

Logged messages and downloaded attachments are organized as follows:

```
Server_Name/                 # Directory for logs from a specific server
├── live_ChannelName.txt     # Log file for a specific channel, containing messages, forward details, and deletion flags
└── attachments/             # (Optional) Directory for downloaded attachments from this channel

DMs/                         # Directory for logs from Direct Messages
├── live_Username_or_GroupName.txt # Log file for a specific DM or group DM
└── attachments/             # (Optional) Directory for downloaded attachments from this DM
```

## Troubleshooting

Here are some common issues and how to resolve them:

*   **Invalid Discord Token:**
    *   **Symptom:** The script fails to log in, or you see errors related to authentication.
    *   **Solution:** If your Discord token becomes invalid or expires, the script is designed to automatically re-prompt you to enter a new token via the GUI. Ensure you are providing a valid user token.

*   **Rate Limiting:**
    *   **Symptom:** The script might temporarily stop fetching messages or encounter errors after running for a while.
    *   **Solution:** Discord imposes rate limits on API requests. As recommended in the warning section, using throwaway or alternative accounts for logging can help mitigate the risk of hitting rate limits on your main account. If you encounter persistent rate limiting, try reducing the frequency of use or switching accounts.

*   **Dependencies Not Found:**
    *   **Symptom:** The script exits with an error like `ModuleNotFoundError: No module named 'aiohttp'` (or `tkinter`, `requests`).
    *   **Solution:** This means one or more required Python packages are not installed. You can install them by running:
        ```bash
        pip install aiohttp tkinter requests
        ```

*   **`tkinter` Not Available:**
    *   **Symptom:** You encounter errors such as `TclError`, `No display name and no $DISPLAY environment variable`, or messages indicating `tkinter` could not be found or initialized, especially when the GUI for token input is expected.
    *   **Solution:** `tkinter` is part of Python's standard library but might be missing in some minimal Python installations (common on Linux servers or specific virtual environments).
        *   On Debian/Ubuntu-based Linux systems, you can usually install it with:
            ```bash
            sudo apt-get update
            sudo apt-get install python3-tk
            ```
        *   For other operating systems or distributions, search for specific instructions to install `tkinter` (or `python3-tk`, `python-tk`) for your Python version.

## Contributing

Contributions to improve this logger are welcome. If you have suggestions for features, find a bug, or want to improve the code, please feel free to open an issue or submit a pull request on the project's repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
