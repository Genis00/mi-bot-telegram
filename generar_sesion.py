import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = 29058204  # tu API ID
API_HASH = "540910880e3367ad8880b3684e92be3e"  # tu API HASH

async def main():
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        print("\n✅ Tu SESSION_STRING generada es:\n")
        print(client.session.save())
        print("\nCopia todo este texto y pégalo en Render como variable de entorno 'SESSION_STRING'")

asyncio.run(main())
