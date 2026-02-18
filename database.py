import psycopg2
import logging

# Настройки подключения к базе данных
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "connectbot2"
DB_USER = "postgres"
DB_PASSWORD = "j5gret52"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Создание подключения к базе данных PostgreSQL"""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return None

def create_users_table():
    """Создание таблицы пользователей, если она не существует"""
    connection = get_db_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            chat_id BIGINT NOT NULL,
            username VARCHAR(255),
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            language_code VARCHAR(10),
            user_type VARCHAR(20) DEFAULT 'user',
            bot_token VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        connection.close()
        logger.info("Таблица пользователей успешно создана или уже существует")
        return True
    except Exception as e:
        logger.error(f"Ошибка при создании таблицы пользователей: {e}")
        if connection:
            connection.close()
        return False

def save_user_info(user, chat_id):
    """Сохранение информации о пользователе в базу данных"""
    connection = get_db_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        # Используем UPSERT (ON CONFLICT) для обновления информации, если пользователь уже существует
        upsert_query = '''
        INSERT INTO users (
            telegram_id, chat_id, username, first_name, last_name, language_code, user_type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (telegram_id)
        DO UPDATE SET
            chat_id = EXCLUDED.chat_id,
            username = EXCLUDED.username,
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            language_code = EXCLUDED.language_code,
            user_type = EXCLUDED.user_type,
            updated_at = CURRENT_TIMESTAMP;
        '''
        
        cursor.execute(upsert_query, (
            user.id,
            chat_id,
            user.username,
            user.first_name,
            user.last_name,
            user.language_code
        ))
        
        connection.commit()
        cursor.close()
        connection.close()
        logger.info(f"Информация о пользователе {user.first_name} успешно сохранена")
        return True
    except Exception as e:
        logger.error(f"Ошибка при сохранении информации о пользователе: {e}")
        if connection:
            connection.close()
        return False