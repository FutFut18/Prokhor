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
    with lock:
        count = (count + 1) % 10
        with open("data1.txt", "w", encoding='utf-8') as data:
            data.write(f"{count} {message.author.global_name} (@" + str(message.author) + "): \n" + str(message.content))

thread2 = threading.Thread(target=scan, name="Thread-2", daemon=True)
thread2.start()

botDS.run(TOKENS)
