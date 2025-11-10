from telethon import TelegramClient
import asyncio
from datetime import datetime
import pytz

api_id = 2040
api_hash = "b18441a1ff607e10a989891a5462e627"
client = TelegramClient("zenx_session", api_id, api_hash)

CHANNEL = "ZenexCrew"
PINNED_MESSAGE_ID = 49

IST = pytz.timezone("Asia/Kolkata")

async def live_time_status():
    entity = await client.get_entity(CHANNEL)
    participants = await client.get_participants(entity)
    total_members = len(participants)
    active_users = sum(1 for u in participants if getattr(u.status, "was_online", None))

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
            print("❌ Error:", e)
            await asyncio.sleep(5)

async def main():
    await client.start()
    print("✅ ZENX Live Clock Started...")
    await live_time_status()

with client:
    client.loop.run_until_complete(main())
