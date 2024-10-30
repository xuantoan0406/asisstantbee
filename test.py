from chatBot.TeleBot import SyntheticBot
from config import settings
a=SyntheticBot(settings.BOT_IP)
a.run_bot()