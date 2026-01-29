from telethon import TelegramClient, events
from telethon.tl.patched import Message
from dotenv import load_dotenv
import asyncio
import os
import sys
from typing import Final
import logging
import subprocess


from database_manager import DatabaseManager

LOG_FORMAT: Final[str] = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

load_dotenv()
API_KEY: Final[int] = int(os.getenv("API_KEY"))
API_HASH: Final[str] = os.getenv("API_HASH")
client = TelegramClient('my_session', API_KEY, API_HASH)

chats: list[str] = ['@mcrepostworld', "@O_Arestovich_official", "@kontext_channel"]



def send_sms(phone: str, text: str) -> None:
    """Отправляет СМС через Termux API."""
    try:
        
        subprocess.run(["termux-sms-send", "-n", phone, text], check=True)
        logger.info(f"СМС успешно отправлено на номер {phone}")
    except Exception as e:
        logger.error(f"Ошибка при отправке СМС: {e}")

@client.on(events.NewMessage(chats=chats))
async def handler(event: events.NewMessage.Event) -> None:
    logger.info("Новое сообщение получено")
    db = DatabaseManager() # Можно вынести инициализацию db выше
    
    msg: Message = event.message
    
    # 1. Проверяем, есть ли текст
    if not msg.text:
        return

    # 2. Проверяем в базе, не обрабатывали ли мы этот пост
    if db.is_post_sent(msg.id):
        return

    # 3. Сохраняем в базу
    if db.save_post(msg.id, msg.chat_id, msg.text):
        logger.info(f"Новый пост обнаружен (ID: {msg.id}). Отправляю СМС...")
        
        # 4. Отправляем СМС (номер возьми из .env)
        friend_phone: str = os.getenv("FRIEND_PHONE", "")
        send_sms(friend_phone, msg.text)

async def main() -> None:
    await client.start()
    logger.info('Бот запущен')

    db = DatabaseManager()
    for chat in chats:
        posts: list[Message]= await client.get_messages(chat, limit=3)
        for post in posts:
            if post.text and not db.is_post_sent(post.id):
                db.save_post(post.id, post.chat_id, post.text, post.chat.title)
    
    logger.info('Бот ожидает новые сообщения...')

    await client.run_until_disconnected()



if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        with client:
            client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.critical(f"Бот упал с ошибкой: {e}", exc_info=True)
    finally:
        logger.info("Сессия закрыта. Программа завершена.")