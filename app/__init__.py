"""
__init__.py

Инициализация пакета app.
"""

# Импортирование настроек логирования
from .log import logger

# Импортирование пула соединений с базой данных
from .database import db_pool  

# Импортирование обработчиков
from .handlers import register_handlers  

__all__ = ["logger", "db_pool", "register_handlers"]  # Определяет, что импортируется при использовании `from app import *`
