#TELEGRAM
import telebot
import time
import threading

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

            if message.reply_to_message:
                try:
                    original_message_text = message.reply_to_message.text.replace('\n',
                                                                                  '')
                    additional_info = f" (ответ на: \"{original_message_text}\")"
                except Exception as e:
                    print(f"Error extracting original message text: {e}")
                    additional_info = ""

            # Запись данных в файл
            with open("data.txt", "w", encoding='utf-8') as data:
                data.write(
                    f"{count} -# {message.from_user.first_name} (@{message.from_user.username}){additional_info}: \n{response_text}\n"
                )


thread5 = threading.Thread(target=scan, name="Thread-5", daemon=True)
thread5.start()
bot.infinity_polling()
