from openai import OpenAI
from config import settings
from utils import read_file_txt


class Assistant:
    def __init__(self, open_api_key):
        self.client = OpenAI(api_key=open_api_key)
        self.content = read_file_txt("chatBot/prompt.txt")
        self.prompt_action = read_file_txt("chatBot/prompt_action.txt")

    def get_answer(self, message: list):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": self.content}] + message
        )
        return response.choices[0].message.content

    def check_action(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": self.prompt_action}]
        )
        return response.choices[0].message.content
