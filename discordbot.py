#DISCORD
import nextcord
import time
import threading
import asyncio

TOKENS = ""

TARGET_CHANNEL_ID = 

intents = nextcord.Intents.default()
intents.message_content = True
botDS = nextcord.Client(intents=intents)
count = 0
lock = threading.Lock()

async def send_message(text):
    channel = botDS.get_channel(TARGET_CHANNEL_ID)
    if channel:
        await channel.send(text)

def scan():
    b = -1
    while True:
        try:
            with open("data.txt", "r", encoding="utf-8") as data:
                content = data.read()

                if content and content[0].isdigit():
                    current = int(content[0])
                    if current != b:
                        b = current
                        global text
                        text = content[1:]
                        asyncio.run_coroutine_threadsafe(send_message(text), botDS.loop)
                time.sleep(0.1)
        except Exception as e:
            print(f"Error during scanning: {e}")
            time.sleep(0.5)

@botDS.event
async def on_message(message):
    if message.author == botDS.user or message.channel.id != TARGET_CHANNEL_ID:
        return

    global count
    additional_info = ""

    if message.reference is not None:
        try:
            original_message = await message.channel.fetch_message(message.reference.message_id)
            original_message_text = original_message.content.replace('\n', '')
            original_message_text = original_message_text.replace('-#', '')
            if original_message.author != botDS.user:
                original_message_author = original_message.author
            else:
                original_message_author = ""
            if original_message_author:
                additional_info = f" (ответ на: {original_message_author}: \"{original_message_text}\")"
            else:
                additional_info = f" (ответ на: \"{original_message_text}\")"
        except Exception as e:
            print(f"Error fetching original message: {e}")
            additional_info = ""

    with lock:
        count = (count + 1) % 10
        with open("data1.txt", "w", encoding='utf-8') as data:
            data.write(
                f"{count} {message.author.global_name} (@" + str(message.author) + f"){additional_info}: \n" + str(message.content)
            )

thread2 = threading.Thread(target=scan, name="Thread-2", daemon=True)
thread2.start()

botDS.run(TOKENS)
