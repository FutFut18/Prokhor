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


async def send_file(file_path):
    channel = botDS.get_channel(TARGET_CHANNEL_ID)

    if channel and os.path.exists(file_path):
        with open(file_path, "rb") as f:
            await channel.send(file=nextcord.File(f, os.path.basename(file_path)))
            os.remove(file_path)
        print(f"Файл '{file_path}' отправлен и удален")
    else:
        print(f"Канал не найден или файл '{file_path}' не существует")


async def send_image_or_file():
    image_path = "image1.jpg"
    if os.path.exists(image_path):
        await send_file(image_path)

    file_extensions = ['zip', 'rar', 'jar', 'txt', 'py', 'java', 'kt', 'pdf', 'exe', 'apk', 'mp3', 'mp4', '7z', 'tar', 'mov', 'webp', 'webm', 'csv', 'json', 'xml', 'html', 'css', 'pptx', 'xlsx', 'docx', 'bmp', 'mkv', 'avi', 'flv', 'wmv', 'sh', 'bat', 'dll', 'rs', 'cpp', 'ogg']

    for ext in file_extensions:
        file_path = f"{ext}1.{ext}"
        if os.path.exists(file_path):
            await send_file(file_path)


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

                    await send_image_or_file()

                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error during scanning: {e}")
            await asyncio.sleep(1)


@botDS.event
async def on_ready():
    print(f"Logged in as {botDS.user}")
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
                image_url = attachment.url
                image_data = requests.get(image_url).content
                save_path = os.path.join("image.jpg")
                with open(save_path, "wb") as f:
                    f.write(image_data)
        for attachment in message.attachments:
            file_mapping = {
                '.zip': 'zip.zip',
                '.rar': 'rar.rar',
                '.jar': 'jar.jar',
                '.txt': 'txt.txt',
                '.py': 'py.py',
                '.java': 'java.java',
                '.kt': 'kt.kt',
                '.pdf': 'pdf.pdf',
                '.exe': 'exe.exe',
                '.apk': 'apk.apk',
                '.mp3': 'mp3.mp3',
                '.mp4': 'mp4.mp4',
                '.7z': '7z.7z',
                '.tar': 'tar.tar',
                '.mov': 'mov.mov',
                '.webp': 'webp.webp',
                '.webm': 'webm.webm',
                '.csv': 'csv.csv',
                '.json': 'json.json',
                '.xml': 'xml.xml',
                '.html': 'html.html',
                '.css': 'css.css',
                '.pptx': 'pptx.pptx',
                '.xlsx': 'xlsx.xlsx',
                '.docx': 'docx.docx',
                '.bmp': 'bmp.bmp',
                '.mkv': 'mkv.mkv',
                '.avi': 'avi.avi',
                '.flv': 'flv.flv',
                '.wmv': 'wmv.wmv',
                '.sh': 'sh.sh',
                '.bat': 'bat.bat',
                '.dll': 'dll.dll',
                '.rs': 'rs.rs',
                '.cpp': 'cpp.cpp',
                '.ogg': 'voice_message.ogg'
            }
            for ext, new_name in file_mapping.items():
                if attachment.filename.endswith(ext):
                    await attachment.save(new_name)
                    break

    count = (count + 1) % 10
    with open("data1.txt", "w", encoding='utf-8') as data:
        data.write(
            f"{count} {message.author.global_name} (@" + str(message.author) + f"){additional_info}: \n" + str(
                message.content)
        )


botDS.run(TOKENS)
