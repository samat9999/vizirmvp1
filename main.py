import os
import telebot
import requests
from flask import Flask

# Твой токен бота
TOKEN = "7561233887:AAH75h7h5cDLBFDOK4QrC7xhsj2nxzIwRkY"
bot = telebot.TeleBot(TOKEN)

# Ссылка на Google Apps Script API
API_URL = "https://script.google.com/macros/s/AKfycbxPYoBVu-tU3hjBA_wsbvTGRsI22O9BdAJqnbuLiJItXyRbo5dmteBOt-YjSvl031mC3g/exec"

# Создаём веб-приложение для Replit
app = Flask(__name__)


@app.route('/')
def home():
    return "Бот работает!"


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для подачи заявок в Визирь. Введите ваше имя:")
    bot.register_next_step_handler(message, get_name)


# Получаем имя клиента
def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Введите ваш номер телефона:")
    bot.register_next_step_handler(message, get_phone, name)


# Получаем телефон
def get_phone(message, name):
    phone = message.text
    bot.send_message(message.chat.id, "Опишите вашу проблему:")
    bot.register_next_step_handler(message, get_question, name, phone)


# Получаем вопрос
def get_question(message, name, phone):
    question = message.text

    # Данные для отправки в Google Sheets
    data = {
        "name": name,
        "phone": phone,
        "question": question,
        "priority": "Обычный",
        "source": "Telegram",
        "deadline": "24 часа",
        "cost": "0"
    }

    # Отправляем в Google Sheets
    response = requests.post(API_URL, json=data)

    if response.text == "Success":
        bot.send_message(
            message.chat.id,
            "✅ Ваша заявка принята! Мы свяжемся с вами в ближайшее время.")
    else:
        bot.send_message(message.chat.id,
                         "❌ Ошибка при отправке заявки. Попробуйте ещё раз.")


# Запускаем веб-приложение в фоне
if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

# Запускаем бота
bot.polling(none_stop=True)
