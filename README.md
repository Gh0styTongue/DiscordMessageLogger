## Discord Message Logger

### ⚠️ User‑Token Only  
- **Bot tokens aren’t supported** you need a real user token.  
- **Create alt/throwaway accounts** to avoid risking your main account.  

### Features  
- **Real‑time logging** of server channels, DMs, and group DMs  
- **Deleted‑message detection**: vanished entries get flagged `[DELETED]` right in your log  
- **Forwarded‑message logging**: fetches the original author/content (or notes if it’s been deleted)  
- **GUI token entry** with automatic saving to `.env` and re‑prompt on invalid tokens  
- **Session separators** (`--- YYYY‑MM‑DD HH:MM:SS ---`) each time you restart  
- **Optional attachment downloads**  

### Setup  
1. Install dependencies:  
   ```bash
   pip install aiohttp tkinter requests
   ```  
2. Run the logger:  
   ```bash
   python logger.py
   ```  
3. Enter your **user token** in the GUI prompt. It’ll be saved to `.env`.  
4. If the token ever fails, you’ll get the GUI again to swap in a fresh one.  

### Usage  
1. Choose **Server** or **DM** mode.  
2. Select your target server→channel or DM thread.  
3. Opt in/out of attachment downloads.  
4. Logging starts immediately—press **Ctrl+C** to stop.  

### Recommended Workflow  
- Spin up a **fresh alt account** for each instance to avoid rate limits or security flags.
- **Coming soon**: built‑in support for **multiple‑instance logging**, so you can monitor several accounts/channels at once.  

### File Layout  
```
Server_Name/
├── live_ChannelName.txt       # your message+forward+deletion log
└── attachments/               # optional downloads
DMs/
├── live_Username.txt
└── attachments/
```  
