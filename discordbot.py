#DISCORD
import nextcord
import asyncio
import os
import time
import requests

TOKENS = ""
TARGET_CHANNEL_ID = 

intents = nextcord.Intents.default()
intents.message_content = True
botDS = nextcord.Client(intents=intents)

count = 0  # Счётчик для сообщений
last_message_time = 0  # Время последнего сообщения
MESSAGE_INTERVAL = 1  # Минимальный интервал в секундах между сообщениями


async def send_message(text):
    channel = botDS.get_channel(TARGET_CHANNEL_ID)
    if channel:
        await channel.send(text)


async def send_image():
    image_path = "image1.jpg"
    channel = botDS.get_channel(TARGET_CHANNEL_ID)

    if channel and os.path.exists(image_path):
        with open(image_path, "rb") as img:
            await channel.send(file=nextcord.File(img, "image1.jpg"))
            os.remove(image_path)
        print(f"Изображение '{image_path}' отправлено и удалено")
    else:
        print(f"Канал не найден или изображение '{image_path}' не существует")


async def scan_file():
    b = -1
    global last_message_time
    while True:
        try:
            with open("data.txt", "r", encoding="utf-8") as data:
                content = data.read()

                if content and content[0].isdigit():
                    current = int(content[0])
                    if current != b:
                        b = current
                        text = content[1:]

                        current_time = time.time()
                        if current_time - last_message_time >= MESSAGE_INTERVAL:
                            await send_message(text)
                            last_message_time = current_time

                    # Проверяем наличие изображения и отправляем, если оно существует
                    if os.path.exists("image1.jpg"):
                        await send_image()

                await asyncio.sleep(1)  # Увеличиваем интервал до 1 сек.
        except Exception as e:
            print(f"Error during scanning: {e}")
            await asyncio.sleep(1)  # Задержка перед новой попыткой


@botDS.event
async def on_ready():
    print(f"Logged in as {botDS.user}")
    # Запускаем асинхронную задачу сканирования файла
    botDS.loop.create_task(scan_file())


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

    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['jpg', 'jpeg', 'png', 'gif']):
                # Скачиваем изображение
                image_url = attachment.url
                image_data = requests.get(image_url).content

                save_path = os.path.join("image.jpg")

                with open(save_path, "wb") as f:
                    f.write(image_data)

    count = (count + 1) % 10
    with open("data1.txt", "w", encoding='utf-8') as data:
        data.write(
            f"{count} {message.author.global_name} (@" + str(message.author) + f"){additional_info}: \n" + str(
                message.content)
        )


botDS.run(TOKENS)
