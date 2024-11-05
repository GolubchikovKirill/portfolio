"""
keyboards.py

Модуль для создания клавиатур и кнопок, используемых ботом.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Что понравилось')],
        [KeyboardButton(text='Что можно добавить')],
        [KeyboardButton(text='Помощь')]
    ],
    resize_keyboard=True
)
