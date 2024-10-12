#TELEGRAM
import telebot
import time
import threading
import os

TOKEN = ""
TGCHATID = ""

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
                        b = current
                        global text
                        text = content[1:]
                        bot.send_message(TGCHATID, text)

                        # Отправка изображения, если оно существует
                        image_path = "image.jpg"
                        if os.path.exists(image_path):
                            with open(image_path, 'rb') as img:
                                bot.send_photo(TGCHATID, img)
                            os.remove(image_path)  # Удаляем изображение после отправки

                time.sleep(0.1)
        except Exception as e:
            print(f"Error during scanning: {e}")
            time.sleep(0.5)

@bot.message_handler()
def accept(message):
    if str(message.chat.id) == TGCHATID:
        global count
        with lock:
            count = (count + 1) % 10

            response_text = message.text.replace('\n', '')
            additional_info = ""

            bot_info = bot.get_me()
            bot_username = bot_info.username

            if message.reply_to_message:
                try:
                    original_message_text = message.reply_to_message.text.replace('\n', '')

                    if message.reply_to_message.from_user.username != bot_username:
                        additional_info = f" (ответ на: @{message.reply_to_message.from_user.username}: \"{original_message_text}\")"
                    else:
                        additional_info = f" (ответ на: \"{original_message_text}\")"

                except Exception as e:
                    print(f"Error extracting original message text: {e}")
                    additional_info = ""

            with open("data.txt", "w", encoding='utf-8') as data:
                data.write(
                    f"{count} -# {message.from_user.first_name} (@{message.from_user.username}){additional_info}: \n{response_text}\n"
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

            with open("image1.jpg", "wb") as new_file:
                new_file.write(downloaded_file)

            print("Изображение сохранено как 'image1.jpg'")

            # Запись информации о фото в data.txt
            with open("data.txt", "w", encoding='utf-8') as data:
                data.write(
                    f"{count} -# {message.from_user.first_name} (@{message.from_user.username}){additional_info}: \n"
                )


thread5 = threading.Thread(target=scan, name="Thread-5", daemon=True)
thread5.start()
bot.infinity_polling()
