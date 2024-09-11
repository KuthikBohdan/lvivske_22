import g4f
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import logging

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Функція для отримання відповіді від моделі
def get_response(prompt):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
            temperature=0.7,
            language='uk'
        )
        full_message = ""
        for message in response:
            full_message += message
        return full_message
    except Exception as e:
        logging.error(f"Error in get_response: {e}")
        return "Вибачте, сталася помилка при отриманні відповіді."

# Функція для обробки текстових повідомлень від користувача
async def handle_message(update: Update, context):
    prompt = update.message.text
    print(f"Запит: {prompt}")  # Виведення запиту в термінал

    if prompt.lower() == "чат стоп":
        await update.message.reply_text("Чат завершено.")
        return
    
    # Отримання відповіді від моделі
    full_message = get_response(prompt)
    print(f"Відповідь: {full_message}")  # Виведення відповіді в термінал

    # Відправка відповіді користувачу в Telegram
    await update.message.reply_text(full_message)

# Основна функція
async def start(update: Update, context):
    await update.message.reply_text("Вітаю! Введіть ваш запит, або 'чат стоп' для завершення.")

if __name__ == "__main__":
    # Створіть бота та підключіться за допомогою вашого токена
    application = ApplicationBuilder().token("7007941774:AAFh7DpDmAb8CeccXA-3jKAtPJMOVgjdtZI").build()

    # Додаємо хендлер для старту та повідомлень
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()
