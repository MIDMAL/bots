import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from database import create_users_table, save_user_info

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота (замените на свой токен)
TOKEN = "8279101693:AAHVWaptKHHRdcWOcJMWdLtENSJZgR49mHc"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(f"Пользователь {user.first_name} запустил бота")
    
    # Сохраняем информацию о пользователе в базу данных
    save_user_info(user, chat_id)
    
    await update.message.reply_text(f'Привет, {user.first_name}!')



# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id
    message_text = update.message.text
    logger.info(f"Пользователь {user.first_name} отправил сообщение: {message_text}")
    
    # Сохраняем информацию о пользователе в базу данных
    save_user_info(user, chat_id)
    
    # Отвечаем "Привет" на любое сообщение
    await update.message.reply_text('Привет!')

def lock() -> None:
    """Заблокировать бота."""
    logger.info("Бот заблокирован")

def main() -> None:
    """Запуск бота."""
    # Создаем таблицу пользователей при запуске
    if create_users_table():
        logger.info("Таблица пользователей успешно создана")
    else:
        logger.error("Не удалось создать таблицу пользователей")
    
    # Создаем Application и передаем ему токен бота
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    logger.info("Бот запущен")
    application.run_polling()

if __name__ == '__main__':
    main()