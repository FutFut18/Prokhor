#DISCORD
import nextcord
import asyncio
import os
import time
import requests
import settings
import re

TOKENS = settings.dstoken
TARGET_CHANNEL_ID = int(settings.dsid)

TG_ID_DIVIDER = settings.TG_ID_DIVIDER
TG_ID_ENDING = settings.TG_ID_ENDING
DS_ID_DIVIDER = settings.DS_ID_DIVIDER
DS_ID_DIVIDER_FORMATTING = settings.DS_ID_DIVIDER_FORMATTING
DS_ID_ENDING = settings.DS_ID_ENDING
MESSAGE_DIVIDER = settings.MESSAGE_DIVIDER
MESSAGE_ENDING = settings.MESSAGE_ENDING
ID_DIVIDER = settings.ID_DIVIDER
ID_ENDING = settings.ID_ENDING
TG_ID_ENDING_ENDING = settings.TG_ID_ENDING_ENDING
DS_ID_ENDING_ENDING = settings.DS_ID_ENDING_ENDING
DS_ID_DIVIDER_DIVIDER = settings.DS_ID_DIVIDER_DIVIDER
webhook_url = settings.webhook_url
file_mapping = settings.file_mapping
server_id = settings.serverid

intents = nextcord.Intents.default()
intents.message_content = True
botDS = nextcord.Client(intents=intents)

count = 0  # Счётчик для сообщений
last_message_time = 0  # Время последнего сообщения
MESSAGE_INTERVAL = 1  # Минимальный интервал в секундах между сообщениями


async def send_message(text, reply_by_id):
    channel = botDS.get_channel(TARGET_CHANNEL_ID)
    if channel and reply_by_id:
        texttoextract = text
        divider = ID_DIVIDER
        ending = ID_ENDING
        idTG = await extract_text(texttoextract, divider, ending)
        if idTG in settings.idZ:
            texttoextract = text
            divider = ID_DIVIDER
            ending = ID_ENDING
            idTG = await extract_text(texttoextract, divider, ending)
            texttoextract = text
            divider = MESSAGE_DIVIDER
            ending = MESSAGE_ENDING
            extracted_text = await extract_text(texttoextract, divider, ending)
            idDS = settings.idZ.get(idTG)
            userDS = await botDS.fetch_user(idDS)
            try:
                avatar = userDS.avatar.url
            except:
                avatar = ""
            texttoextract = text
            divider = TG_ID_DIVIDER
            ending = TG_ID_ENDING
            idMSG = await extract_text(texttoextract, divider, ending)
            extracted_text += TG_ID_DIVIDER
            extracted_text += idMSG
            extracted_text += TG_ID_ENDING
            link = "-# https://discord.com/channels/" + server_id + "/" + str(TARGET_CHANNEL_ID) + "/" + str(reply_by_id) + "\n"
            print(reply_by_id)
            data = {
                "content": link + extracted_text,
                "username": userDS.name,
                "avatar_url": avatar,
                "message_reference": {
                    "message_id": reply_by_id,
                    "channel_id": TARGET_CHANNEL_ID,
                }
            }
            send_webhook = requests.post(webhook_url, json=data)
        else:
            text = text.replace(MESSAGE_DIVIDER, "")
            text = text.replace(MESSAGE_ENDING, "")
            texttoremove = text
            divider = ID_DIVIDER
            ending = ID_ENDING
            text = await remove_sections(texttoremove, divider, ending)
            reply_to = await channel.fetch_message(reply_by_id)
            await reply_to.reply(text)
    elif channel:
        texttoextract = text
        divider = ID_DIVIDER
        ending = ID_ENDING
        idTG = await extract_text(texttoextract, divider, ending)
        if idTG in settings.idZ:
            texttoextract = text
            divider = MESSAGE_DIVIDER
            ending = MESSAGE_ENDING
            extracted_text = await extract_text(texttoextract, divider, ending)
            idDS = settings.idZ.get(idTG)
            userDS = await botDS.fetch_user(idDS)
            try:
                avatar = userDS.avatar.url
            except:
                avatar = ""
            texttoextract = text
            divider = TG_ID_DIVIDER
            ending = TG_ID_ENDING
            idMSG = await extract_text(texttoextract, divider, ending)
            extracted_text += TG_ID_DIVIDER
            extracted_text += idMSG
            extracted_text += TG_ID_ENDING
            data = {
                "content": extracted_text,
                "username": userDS.name,
                "avatar_url": avatar
            }

            response = requests.post(webhook_url, json=data)
        else:
            text = text.replace(MESSAGE_DIVIDER, "")
            text = text.replace(MESSAGE_ENDING, "")
            texttoremove = text
            divider = ID_DIVIDER
            ending = ID_ENDING
            text = await remove_sections(texttoremove, divider, ending)
            await channel.send(text)

async def extract_text(texttoextract: str, divider: str, ending: str) -> str:
    try:
        start = texttoextract.index(divider) + len(divider)
        end = texttoextract.index(ending, start)
        return texttoextract[start:end].strip()
    except ValueError:
        return ""

async def remove_sections(texttoremove: str, divider: str, ending: str) -> str:
    pattern = re.escape(divider) + r'.*?' + re.escape(ending)
    cleaned_text = re.sub(pattern, '', texttoremove)
    return cleaned_text

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
                        origid = False
                        b = current
                        text = content[1:]
                        try:
                            text, origid = text.split(DS_ID_DIVIDER) # ГОВНОКОДИЩЕ
                            origid = int(origid,16)
                        except ValueError:
                            text = text
                        current_time = time.time()
                        if current_time - last_message_time >= MESSAGE_INTERVAL:
                            await send_message(text, origid)
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
    identificators = f"{DS_ID_DIVIDER_FORMATTING}{hex(message.id)[2:]}{DS_ID_ENDING}`"
    if message.reference is not None:
        try:
            original_message = await message.channel.fetch_message(message.reference.message_id)
            origtext = original_message.content
            origauthor = original_message.author
            origid = ""
            if origauthor != botDS.user:
                origauthor = original_message.author
                origtext = original_message.content
            else:
                origauthor = ""
                try:
                    origtext, origid = origtext.split(TG_ID_DIVIDER)
                except ValueError:
                    origtext = origtext
            if origid:
                identificators += f"{TG_ID_DIVIDER}{origid[:-1]}"
            else:
                additional_info = f" (ответ на: \"{origtext}\")"
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
            for ext, new_name in file_mapping.items():
                if attachment.filename.endswith(ext):
                    await attachment.save(new_name)
                    break

    count = (count + 1) % 10
    with open("data1.txt", "w", encoding='utf-8') as data:
        message_author = str(message.author)
        message_author = message_author.replace('*', '\*')
        message_author = message_author.replace('_', '\_')
        message_author = message_author.replace('`', '\`')
        message.content = str(message.content)
        message.content = message.content.replace('`', '\`')
        message.content = message.content.replace('*', '\*')
        message.content = message.content.replace('_', '\_')
        additional_info = str(additional_info)
        additional_info = additional_info.replace('`', '\`')
        additional_info = additional_info.replace('_', '\_')
        additional_info = additional_info.replace('*', '\*')
        data.write(
            f"{count} @{message_author}{additional_info}: " + str(message.content) + f"{identificators}"
        )

botDS.run(TOKENS)
