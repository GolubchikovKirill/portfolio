"""
log.py

Настройки для логирования.
"""

import logging

# Настройки логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Логирование в файл
        logging.StreamHandler()  # Логирование в консоль
    ]
)

# Создание логгера
logger = logging.getLogger(__name__)  # Получение логгера с именем текущего модуля

