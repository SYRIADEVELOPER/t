import json
from telethon import TelegramClient, events

# ضع توكن البوت هنا
bot_token = "8249193765:AAFD3IjSCEAkfqwViXHRgRprYQksYZj6E_E"

# قراءة القنوات والكلمات المحظورة من config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

source_channels = config["source_channels"]
target_channel = config["target_channel"]
blocked_words = [w.lower() for w in config["blocked_words"]]

# إنشاء العميل باستخدام البوت مباشرة
client = TelegramClient('forwarder', api_id=0, api_hash='').start(bot_token=bot_token)

def is_clean(text: str) -> bool:
    if not text:
        return True
    text_lower = text.lower()
    for word in blocked_words:
        if word in text_lower:
            return False
    return True

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    message_text = event.message.message or ""
    if is_clean(message_text):
        try:
            await client.forward_messages(target_channel, event.message)
            print(f"✅ Forwarded: {message_text[:50]}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"🚫 Blocked message: {message_text[:50]}")

print("🚀 Bot is running...")
client.run_until_disconnected()
