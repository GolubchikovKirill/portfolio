"""
Точка входа для запуска Telegram бота.
Инициализирует бота, диспетчера и подключает обработчики сообщений.
"""

import logging
import asyncio
import os
import pandas as pd  # Импортируем библиотеку pandas
from pathlib import Path
from aiogram import Bot, Dispatcher
from app.handlers import register_handlers
from dotenv import load_dotenv
from app import log  # Импортирование настроек логирования
from app.database import fetch_data, init_db_pool  # Импортируем функции для работы с БД

# Загрузка переменных окружения из файла .env
load_dotenv()

# Логирование с использованием настроек из log.py
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Получение токена бота из переменных окружения
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    logger.error("Токен Telegram бота не найден в переменных окружения.")
    raise ValueError("Переменная окружения TELEGRAM_BOT_TOKEN не задана")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def export_data_to_csv():
    """Экспорт данных из базы данных в файл data.csv."""
    logger.info("Начало экспорта данных в CSV...")
    
    try:
        # Извлечение данных из базы данных
        data = await fetch_data()  # Предполагается, что эта функция возвращает список словарей

        if data:  # Проверяем, есть ли данные для экспорта
            # Создаем DataFrame из полученных данных
            df = pd.DataFrame(data)

            # Убедитесь, что папка app существует
            app_path = Path(__file__).parent
            csv_file_path = app_path / "data.csv"

            # Запись данных в CSV файл
            df.to_csv(csv_file_path, index=False, encoding='utf-8')
            logger.info(f"Данные успешно экспортированы в {csv_file_path}")
        else:
            logger.warning("Нет данных для экспорта в CSV.")

    except Exception as e:
        logger.error(f"Ошибка при экспорте данных: {e}")

async def main():
    # Инициализация пула соединений с базой данных
    await init_db_pool()  
    logger.info("Бот запущен и готов к приему сообщений.")
    register_handlers(dp)
    
    # Экспорт данных перед началом опроса
    await export_data_to_csv()
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Ошибка при запуске бота: %s", e)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logger.info("Запуск основного приложения...")
    asyncio.run(main())













