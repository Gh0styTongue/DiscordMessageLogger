⚠️ **Warning**: This script logs messages in real‑time from Discord servers, channels, and DMs. You must follow Discord’s Terms of Service and respect user privacy.  

## Discord Message Logger

### Features
- Log messages from **servers** or **direct messages** (DMs & group DMs)  
- **Deleted‑message detection**: flags vanished messages in the log with `[DELETED]`  
- **Forwarded‑message detection**: retrieves and logs the original author/content (or notes if it’s been deleted)  
- **Attachment downloads** (optional)  
- **GUI token entry** with secure `.env` storage and automatic re‑prompt if the token is invalid  
- **Session‑based log splitting**: when you restart, a timestamp separator (`--- YYYY‑MM‑DD HH:MM:SS ---`) marks new runs  
- Sanitizes filenames and directory names automatically  

### Legal Requirements
- Comply with [Discord ToS](https://discord.com/terms)  
- Obtain proper permissions for logging  
- Never log private conversations without consent  
- **Bot tokens** are strongly recommended over user tokens  

## Setup
1. **Install**  
   ```bash
   pip install aiohttp
   ```
2. **Run**  
   ```bash
   python logger.py
   ```
   - On first launch you’ll get a GUI prompt to enter your token; it’s saved to `.env`.  
   - If the token ever fails, the GUI re‑appears to let you update it.  

## Usage
1. Choose **Server Channels** or **DMs**  
2. Select your target (server → channel, or DM thread)  
3. Opt in or out of downloading attachments  
4. Logging begins immediately; press `Ctrl+C` to stop  

## Changelog

### New Additions
- **Forwarded message logging**: fetches original author/content when possible  
- **Log session separators**: clearly split runs with `--- YYYY‑MM‑DD HH:MM:SS ---`  
- **GUI & `.env` token management**: enter once, auto‑save, and re‑prompt on invalid tokens  
- **Deleted‑message flagging**: appends `[DELETED]` in place within your existing log  
- Full support for **DMs & group DMs**  
- Removed message‑editing tracking to streamline logs  

## File Structure
```
Server_Name/
├── live_ChannelName.txt     # your message log, with session splits
└── attachments/             # optional downloads
DMs/
├── live_Username.txt
└── attachments/
```

**Always inform participants when logging conversations!**
