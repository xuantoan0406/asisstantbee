import telebot
import hashlib
import time
from config import settings
from db.RedisPool import RedisPool
from chatBot.Assistant import Assistant
# from chatBot.GenerateImage import GenerateImage


class SyntheticBot:
    def __init__(self, bot_token):
        self.bot = telebot.TeleBot(bot_token)
        self.redis_pool = RedisPool(settings.REDIS_HOST, settings.REDIS_PORT, 0, 100)
        self.assistant = Assistant(settings.OPENAI_API_KEY)
        # self.generate_image = GenerateImage()

    @staticmethod
    def create_name_image():
        unique_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
        return unique_id

    # Implement image generation logic here

    def run_bot(self):
        # @self.bot.message_handler(commands=['ls'])
        # def handle_list_docs(message):
        #     document_list = ['🪩 *Usage*:',
        #                      '🔸 /q      Virtual assistant. *Ex* :/q what it? ',
        #                      '🔸 /img    create an image from text. *Ex* : /img 1 girl ',
        #                      '🔸 /s      summarize text, website . *Ex* : "abc.com",  "text a paper"',
        #                      '🔸 /ytb      summarize content youtube. *Ex* : "https://www.youtube.com/watch?v=Ajads"']
        #
        #     self.bot.send_message(message.chat.id, '\n'.join(document_list), parse_mode='Markdown')
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            user_id = message.from_user.id
            self.bot.reply_to(message, f"Hello! Your user ID is {user_id}. How can I help you today?")

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        def echo_message(message):
            user_id = message.from_user.id
            self.redis_pool.add_conversation(user_id, 'user', message.text)
            chat_history = self.redis_pool.get_conversation_history(user_id)
            answer = self.assistant.get_answer(chat_history)
            check_image = self.assistant.check_action()
            if check_image.isdigit():
                print(check_image)
                if int(check_image) == 1 or int(check_image == 0):
                    image_name = self.create_name_image()
                    # self.generate_image.generate_image(message.text, image_name)
                    self.bot.send_chat_action(message.chat.id, 'upload_photo')
                    self.bot.send_photo(message.chat.id, open('images/2530064.png', 'rb'))

            print(chat_history)
            self.redis_pool.add_conversation(user_id, 'assistant', answer)
            self.bot.reply_to(message, answer)

        self.bot.infinity_polling(timeout=10, long_polling_timeout=5)

# a = SyntheticBot(settings.BOT_IP)
# a.run_bot()
# import telebot
# # Replace 'YOUR_TOKEN' with your bot's token from BotFather
# TOKEN = settings.BOT_IP
# bot = telebot.TeleBot(TOKEN)
# # Handler for /start command
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     user_id = message.from_user.id
#     bot.reply_to(message, f"Hello! Your user ID is {user_id}. How can I help you today?")
#
#
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_message(message):
#     user_id = message.from_user.id
#     bot.reply_to(message, f"Your user ID is {user_id}. You said: {message.text}")
#
# # Run the bot
# print("Bot is running...")
# bot.infinity_polling()
