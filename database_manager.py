import logging
import sqlite3
from datetime import datetime
from typing import Final, Optional

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, db_path: str = "news_archive.db") -> None:
        self.db_path: Final[str] = db_path
        self._create_table()
        logger.info("База данных инициализирована")

    def _create_table(self) -> None:
        """Создает таблицу, если она еще не существует."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    message_id INTEGER PRIMARY KEY,
                    channel_id INTEGER, 
                    text TEXT,
                    timestamp DATETIME
                )
            """)
            conn.commit()
            logger.info("База данных создана")

    def save_post(
        self, msg_id: int, chat_id: int, text: Optional[str], chat_name: str
    ) -> bool:
        """
        Сохраняет пост в базу.
        Возвращает True, если сохранен, и False, если такой ID уже есть.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO posts (message_id, channel_id, text, timestamp) VALUES (?, ?, ?, ?)",
                    (msg_id, chat_id, text, datetime.now()),
                )
                logger.info(f"Пост от {chat_name} сохранён в базу данных")
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            logger.info("Пост уже есть в базе данных")
            # Сработает, если message_id уже существует (PRIMARY KEY)
            return False

    def is_post_sent(self, msg_id: int) -> bool:
        """Проверяет, был ли этот пост уже обработан."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM posts WHERE message_id = ?", (msg_id,))
            return cursor.fetchone() is not None
