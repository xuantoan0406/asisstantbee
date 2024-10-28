import telebot
import hashlib
import time
from config import settings


class SyntheticBot:

    def __init__(self, bot_token):
        self.bot = telebot.TeleBot(bot_token)

    @staticmethod
    def create_name_image():
        unique_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
        return unique_id

    def run_bot(self):
        @self.bot.message_handler(commands=['ls'])
        def handle_list_docs(message):
            document_list = ['🪩 *Usage*:',
                             '🔸 /q      Virtual assistant. *Ex* :/q what it? ',
                             '🔸 /img    create an image from text. *Ex* : /img 1 girl ',
                             '🔸 /s      summarize text, website . *Ex* : "abc.com",  "text a paper"',
                             '🔸 /ytb      summarize content youtube. *Ex* : "https://www.youtube.com/watch?v=Ajads"']

            self.bot.send_message(message.chat.id, '\n'.join(document_list), parse_mode='Markdown')

        @self.bot.message_handler(commands=['img'])
        def generate_image(message):
            cid = message.chat.id
            self.bot.send_chat_action(cid, 'typing')
            prompt = message.text.replace('/img', '')
            unique_id = self.create_name_image()
            self.GenImage.generateImage(prompt, unique_id)
            self.bot.send_chat_action(cid, 'typing')
            self.bot.send_photo(str(cid),
                                photo=open(f'App/generateImage/Image/{unique_id}.png', 'rb'))
            self.bot.reply_to(message, prompt, parse_mode='HTML')

        self.bot.infinity_polling(timeout=10, long_polling_timeout=5)




a = SyntheticBot(settings.BOT_IP)
a.run_bot()
