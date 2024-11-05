"""
handlers.py

Модуль, содержащий обработчики команд и сообщений.
Подключается к основному приложению для обработки сообщений и команд от пользователей.
"""

from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram import F  # Импортируем F для фильтров
from aiogram.filters import Command
from app.database import save_feedback
from app.keyboards import keyboard
import logging

async def handle_start(message: Message):
    """Обработчик команды /start."""
    logging.info(f"Пользователь @{message.from_user.username} отправил команду /start")
    await message.answer(
        "Уважаемые студенты! Я бот для сбора обратной связи. "
        "Поделитесь тем, что вам понравилось и что вы хотели бы добавить.\n"
        "Выберите одну из кнопок ниже и отправьте ваше сообщение.",
        reply_markup=keyboard
    )

async def handle_help(message: Message):
    """Обработчик команды /help и кнопки 'Помощь'."""
    logging.info(f"Пользователь @{message.from_user.username} запросил помощь.")
    help_text = (
        "Я бот, моя цель — сбор обратной связи.\n"
        "Вот что я умею:\n"
        "- Кнопка 'Что понравилось' — для описания того, что больше всего запомнилось.\n"
        "- Кнопка 'Что можно добавить' — для предложений и идей.\n"
        "- Кнопка 'Помощь' или команда /help — для получения информации о функциях бота.\n"
        "Используйте эти кнопки, чтобы быстро отправить свои отзывы!"
    )
    await message.answer(help_text)

async def handle_feedback_request(message: Message):
    """Обработчик кнопок 'Что понравилось' и 'Что можно добавить'."""
    feedback_type = 'Like it:' if message.text == 'Что понравилось' else 'Add:'
    logging.info(f"Пользователь @{message.from_user.username} нажал кнопку '{feedback_type}'")
    await message.answer(f"Напишите ваше сообщение для раздела '{feedback_type}'.")

async def handle_feedback(message: Message):
    """Обработчик текстовых сообщений с отзывами."""
    username = message.from_user.username or "Без никнейма"
    user_id = message.from_user.id
    feedback = message.text
    logging.info(f"Получено сообщение от пользователя @{username} с user_id={user_id}: {feedback}")

    # Определяем тип обратной связи на основе текста ответа
    feedback_type = 'Add:'
    if message.reply_to_message:
        if 'Like it:' in message.reply_to_message.text:
            feedback_type = 'Like it:'
        elif 'Add:' in message.reply_to_message.text:
            feedback_type = 'Add:'

    # Проверяем, если сообщение отвечает на запрос помощи
    if message.reply_to_message and 'Помощь' in message.reply_to_message.text:
        logging.info(f"Пользователь @{username} ответил на запрос помощи, не отправляем благодарность.")
        return  # Не отправляем благодарность, если это ответ на помощь

    # Вызов асинхронной функции с использованием await
    await save_feedback(username, feedback_type, feedback, user_id)  # Изменено: добавлено await
    await message.answer("Благодарим за обратную связь!")

def register_handlers(dp: Dispatcher):
    """Регистрирует обработчики в диспетчере."""
    dp.message.register(handle_start, Command("start"))
    dp.message.register(handle_help, Command("help"))
    dp.message.register(handle_feedback_request, F.text.in_(['Что понравилось', 'Что можно добавить']))  # Используем F для фильтров
    dp.message.register(handle_feedback, F.text)  # Регистрация обработчика текстовых сообщений


