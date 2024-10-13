#TELEGRAM
import telebot
import time
import threading
import os

TOKEN = ""
TGCHATID = ""

TG_ID_DIVIDER = "\n-# [t^"
TG_ID_ENDING = "]"
DS_ID_DIVIDER = "\n [d^"
DS_ID_ENDING = "]"

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
                                #text = text.replace('_', '\_')
                                #text = text.replace('*', '\*')
                                #text = text.replace('`', '\`')
                                bot.send_message(TGCHATID, text, reply_parameters=telebot.types.ReplyParameters(message_id=origid), parse_mode='Markdown')
                            except:
                                print("разрабы дауны")
                                bot.send_message(TGCHATID, text, reply_parameters=telebot.types.ReplyParameters(message_id=origid))
                        else:
                            try:
                                #text = text.replace('_', '\_')
                                #text = text.replace('*', '\*')
                                #text = text.replace('`', '\`')
                                bot.send_message(TGCHATID, text, parse_mode='Markdown')
                            except:
                                print("разрабы дауны")
                                bot.send_message(TGCHATID, text)

                        image_path = "image.jpg"
                        if os.path.exists(image_path):
                            with open(image_path, 'rb') as img:
                                bot.send_photo(TGCHATID, img)
                            os.remove(image_path)
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
                    f"{count} @{message.from_user.username}{additional_info}: {response_text}{identificators}"
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

            # Сохраняем фото
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Проверяем размер файла
            if len(downloaded_file) > 10 * 1024 * 1024:  # 10 MB
                bot.send_message(TGCHATID, "Файл слишком большой для Discord.")
                return  # Не сохраняем файл, если он слишком большой

            with open("image1.jpg", "wb") as new_file:
                new_file.write(downloaded_file)

            print("Изображение сохранено как 'image1.jpg'")

            # Запись информации о фото в data.txt
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

            # Проверяем размер файла
            if len(downloaded_file) > 10 * 1024 * 1024:  # 10 MB
                bot.send_message(TGCHATID, "Файл слишком большой для Discord.")
                return  # Не сохраняем файл, если он слишком большой

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
