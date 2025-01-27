# Discord Message Logger (Beta)

⚠️ **Beta Notice**: This is a beta version of the Discord Message Logger. Features may be unstable or subject to change. Provide feedback via GitHub Issues.

**Warning**: This script logs messages in real-time from Discord servers, channels, and DMs. You must follow Discord's Terms of Service (ToS) and respect user privacy.

## Features
- Log messages from **servers** or **direct messages** (DMs)
- Capture deleted messages (if permissions allow)
- Download attachments
- Supports both bot tokens and user tokens (⚠️ **risky**)
- Organized logging structure:
  ```
  Server_Name/
  ├── live_ChannelName.txt
  └── attachments/
  DMs/
  ├── live_Username.txt
  └── attachments/
  ```

## Legal Requirements
- **Comply with [Discord ToS](https://discord.com/terms)**
- Obtain proper permissions for logging
- Never log private conversations without consent
- Bot tokens preferred over user tokens

```diff
- Using user tokens for automation violates Discord's ToS!
- Misuse may result in account termination!
```

## Setup
1. **Install requirements**:
   ```bash
   pip install aiohttp
   ```

2. **Configure token**:
   ```python
   # In logging-beta.py
   TOKEN = "YOUR_TOKEN_HERE"  # Bot token recommended
   ```

## Usage
```bash
python logging-beta.py
```

**Workflow**:
1. Choose between server channels or DMs
2. Select target server/channel or DM conversation
3. Enable/disable attachment downloading
4. Logging starts automatically

**Controls**:
- `Ctrl+C` to stop logging
- Automatic cleanup of invalid filename characters

## Beta Notes
- New DM logging feature
- Experimental attachment handling
- Rate limits not fully implemented
- Report issues with:
  - Group DM detection
  - Long-running sessions
  - Attachment downloads

## Key Updates
```diff
+ Added DM/Group DM support
+ Improved filename sanitization
+ Better error handling for attachments
- Removed message editing tracking
```

## Functions
| Function | Description |
|----------|-------------|
| `select_server()` | Choose server from list |
| `select_dm_channel()` | Pick DM/conversation |
| `clean_name()` | Safe filename creation |
| `log_messages_from_current()` | Core logging handler |
| `download_attachment()` | Media backup (optional) |

## Warnings
1. **Attachments** may expose personal data
2. **Deleted messages** remain in logs
3. **DM logging** requires extreme caution
4. **Beta software** - may contain bugs

**Always inform participants when logging conversations!**

---

**Report bugs**: [GitHub Issues]  
**License**: Include proper licensing information here
