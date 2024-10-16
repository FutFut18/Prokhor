#TELEGRAM
import telebot
import time
import threading
import os
import settings

TOKEN = settings.tgtoken
TGCHATID = settings.tgid

TG_ID_DIVIDER = settings.TG_ID_DIVIDER
TG_ID_ENDING = settings.TG_ID_ENDING
DS_ID_DIVIDER = settings.DS_ID_DIVIDER
DS_ID_ENDING = settings.DS_ID_ENDING
MESSAGE_DIVIDER = settings.MESSAGE_DIVIDER
MESSAGE_ENDING = settings.MESSAGE_ENDING
ID_DIVIDER = settings.ID_DIVIDER
ID_ENDING = settings.ID_ENDING
TG_ID_ENDING_ENDING = settings.TG_ID_ENDING_ENDING
DS_ID_ENDING_ENDING = settings.DS_ID_ENDING_ENDING
DS_ID_DIVIDER_DIVIDER = settings.DS_ID_DIVIDER_DIVIDER
file_mapping = settings.file_mapping
bot = telebot.TeleBot(TOKEN)
count = 0
lock = threading.Lock()

def scan():
    b = -1
    while True:
        try:
            with open("data1.txt", "r", encoding="utf-8") as data:
                content = data.read()

                if content and content[0].isdigit():
                    current = int(content[0])
                    if current != b:
                        origid = False
                        b = current
                        global text
                        text = content[1:]
                        try:
                            text, origid = text.split(TG_ID_DIVIDER) # govnokod
                        except ValueError:
                            text = text
                        if origid:
                            try:
                                print(origid)
                                bot.send_message(TGCHATID, text, reply_parameters=telebot.types.ReplyParameters(message_id=origid), parse_mode='Markdown')
                            except:
                                print(origid)
                                bot.send_message(TGCHATID, text, reply_parameters=telebot.types.ReplyParameters(message_id=origid))
                        else:
                            try:
                                print(origid)
                                bot.send_message(TGCHATID, text, parse_mode='Markdown')
                            except:
                                print(origid)
                                bot.send_message(TGCHATID, text)

                        image_path = "image.jpg"
                        if os.path.exists(image_path):
                            with open(image_path, 'rb') as img:
                                bot.send_photo(TGCHATID, img)
                            os.remove(image_path)
                        for ext, file_name in file_mapping.items():
                            if os.path.exists(file_name):
                                with open(file_name, 'rb') as f:
                                    bot.send_document(TGCHATID, f)
                                os.remove(file_name)


                time.sleep(0.1)
        except Exception as e:
            print(f"Error during scanning: {e}")
            time.sleep(0.5)

def save_file_with_index(file_extension, count, file_data):
    if file_extension in file_mapping:
        new_file_name = file_mapping[file_extension].replace('.', '1.')
    else:
        new_file_name = f'file1{file_extension}'

    with open(new_file_name, "wb") as new_file:
        new_file.write(file_data)

    print(f"Файл сохранён как '{new_file_name}'")
    return new_file_name


@bot.message_handler()
def accept(message):
    if str(message.chat.id) == TGCHATID:
        global count
        with lock:
            count = (count + 1) % 10

            response_text = message.text.replace('\n', '')
            additional_info = ""
            origtext = ""
            origid = ""

            bot_info = bot.get_me()
            bot_username = bot_info.username
            identificators = f"{TG_ID_DIVIDER}{message.id}{TG_ID_ENDING}"

            if message.reply_to_message:
                try:
                    origtext = message.reply_to_message.text

                    if message.reply_to_message.from_user.username != bot_username:
                        additional_info = f" (ответ на: {message.reply_to_message.from_user.username}: \"{origtext}\")"
                    else:
                        try:
                            origtext, origid = message.reply_to_message.text.split(DS_ID_DIVIDER)
                        except ValueError:
                            origtext = origtext.replace('\n', '')
                        if origid:
                            identificators += f"{DS_ID_DIVIDER}{origid[:-1]}"
                        else:
                            additional_info = f" (ответ на: \"{origtext}\")"

                except Exception as e:
                    print(f"Error extracting original message text: {e}")
                    additional_info = ""

            with open("data.txt", "w", encoding='utf-8') as data:
                data.write(
                    f"{count} @{message.from_user.username}{additional_info}: {ID_DIVIDER}{message.from_user.id}{ID_ENDING}{MESSAGE_DIVIDER}{response_text}{MESSAGE_ENDING}{identificators}"
                )

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if str(message.chat.id) == TGCHATID:
        global count
        with lock:
            count = (count + 1) % 10

            additional_info = ""
            bot_info = bot.get_me()
            bot_username = bot_info.username

            if message.reply_to_message:
                try:
                    original_message_text = message.reply_to_message.text.replace('\n', '') if message.reply_to_message.text else "<no text>"

                    if message.reply_to_message.from_user.username != bot_username:
                        additional_info = f" (ответ на: @{message.reply_to_message.from_user.username}: \"{original_message_text}\")"
                    else:
                        additional_info = f" (ответ на: \"{original_message_text}\")"

                except Exception as e:
                    print(f"Error extracting original message text: {e}")
                    additional_info = ""

            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            if len(downloaded_file) > 10 * 1024 * 1024:  # 10 MB
                bot.send_message(TGCHATID, "Файл слишком большой для Discord.")
                return

            with open("image1.jpg", "wb") as new_file:
                new_file.write(downloaded_file)

            print("Изображение сохранено как 'image1.jpg'")

            with open("data.txt", "w", encoding='utf-8') as data:
                data.write(
                    f"{count} @{message.from_user.username}{additional_info}: "
                )

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if str(message.chat.id) == TGCHATID:
        global count
        with lock:
            count = (count + 1) % 10

            additional_info = ""
            bot_info = bot.get_me()
            bot_username = bot_info.username

            if message.reply_to_message:
                try:
                    original_message_text = message.reply_to_message.text.replace('\n', '') if message.reply_to_message.text else "<no text>"

                    if message.reply_to_message.from_user.username != bot_username:
                        additional_info = f" (ответ на: @{message.reply_to_message.from_user.username}: \"{original_message_text}\")"
                    else:
                        additional_info = f" (ответ на: \"{original_message_text}\")"
                except Exception as e:
                    print(f"Error extracting original message text: {e}")
                    additional_info = ""
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            if len(downloaded_file) > 10 * 1024 * 1024:  # 10 MB
                bot.send_message(TGCHATID, "Файл слишком большой для Discord.")
                return
            file_extension = os.path.splitext(message.document.file_name)[1]
            saved_file_name = save_file_with_index(file_extension, count, downloaded_file)
            print(f"Файл был сохранён как: {saved_file_name}")
            with open("data.txt", "w", encoding='utf-8') as data:
                data.write(
                    f"{count} @{message.from_user.username}{additional_info}: "
                )

thread5 = threading.Thread(target=scan, name="Thread-5", daemon=True)
thread5.start()
bot.infinity_polling()
