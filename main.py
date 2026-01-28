from aiogram import executor, Bot, Dispatcher, types
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN_API = os.getenv("TOKEN")


bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)

if __name__ == "__main__":
    ...
