"""
Модуль для работы с базой данных PostgreSQL.
Создает пул соединений и предоставляет функции для сохранения данных.
"""

import asyncpg
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Параметры подключения к базе данных
DB_PARAMS = {
    'database': os.getenv("DB_NAME"),  # Изменено на 'database'
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT", "5432")  # Порт по умолчанию
}

# Создание пула соединений
db_pool = None

async def init_db_pool():
    """Инициализация пула соединений к базе данных."""
    global db_pool
    try:
        db_pool = await asyncpg.create_pool(**DB_PARAMS)
        logging.info("Пул соединений с базой данных успешно создан.")
    except Exception as e:
        logging.error(f"Ошибка при создании пула соединений: {e}")
        raise

async def save_feedback(username, feedback_type, feedback, user_id):
    """Сохраняет обратную связь в базу данных."""
    try:
        async with db_pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO feedback_schema.feedback (username, feedback, message_time, user_id)
                VALUES ($1, $2, $3, $4);
                """,
                username, f"{feedback_type} {feedback}", datetime.now(), user_id
            )
            logging.info("Отзыв успешно сохранен в базу данных.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении отзыва: {e}")

async def fetch_data():
    """Извлечение данных из базы данных."""
    try:
        async with db_pool.acquire() as connection:
            rows = await connection.fetch("SELECT username, feedback, message_time FROM feedback_schema.feedback;")
            logging.info("Данные успешно извлечены из базы данных.")
            return [{"username": row['username'], "feedback": row['feedback'], "message_time": row['message_time']} for row in rows]
    except Exception as e:
        logging.error(f"Ошибка извлечения данных: {e}")
        return []

