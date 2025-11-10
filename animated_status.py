import os
import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient

# -------------------------
# CONFIGURATION
# -------------------------

api_id = 2040
api_hash = "b18441a1ff607e10a989891a5462e627"
bot_token = "8239402267:AAFz8pVgZ70BrArslcwPrnYifelnBBsnJfc"

SESSION_NAME = "zenx_session"

CHANNEL = "ZenexCrew"       # Channel username (no @)
PINNED_MESSAGE_ID = 49      # Pinned message ID

IST = pytz.timezone("Asia/Kolkata")  # Indian Standard Time

# -------------------------
# SESSION HANDLING
# -------------------------

# Remove old/corrupted session file if exists
if os.path.exists(f"{SESSION_NAME}.session"):
    os.remove(f"{SESSION_NAME}.session")

# -------------------------
# TELEGRAM CLIENT
# -------------------------

# Start client with bot token (non-interactive)
client = TelegramClient(SESSION_NAME, api_id, api_hash).start(bot_token=bot_token)

# -------------------------
# LIVE STATUS FUNCTION
# -------------------------

async def live_time_status():
    try:
        entity = await client.get_entity(CHANNEL)
        participants = await client.get_participants(entity)
        total_members = len(participants)
        active_users = sum(1 for u in participants if getattr(u.status, "was_online", None))
    except Exception as e:
        print("❌ Error fetching channel info:", e)
        total_members = 0
        active_users = 0

    while True:
        try:
            now_ist = datetime.now(IST)
            time_str = now_ist.strftime("%I:%M:%S %p")
            day_str = now_ist.strftime("%A")

            text = f"""
🔥 **ZENX AUTO STATUS LIVE** 🔥
━━━━━━━━━━━━━━
👥 Members: `{total_members}`
🟢 Active: `{active_users}`
🕒 Time: `{time_str}` | 📅 {day_str}
━━━━━━━━━━━━━━
⚡ Live Status Updating About ZenX Channel...
"""
            await client.edit_message(CHANNEL, PINNED_MESSAGE_ID, text)
            await asyncio.sleep(1)

        except Exception as e:
            print("❌ Error updating message:", e)
            await asyncio.sleep(5)

# -------------------------
# MAIN
# -------------------------

async def main():
    print("✅ ZENX Live Clock (IST) Started...")
    await live_time_status()

# -------------------------
# RUN CLIENT
# -------------------------

with client:
    client.loop.run_until_complete(main())
