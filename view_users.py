import psycopg2
from database import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def get_users():
    """Получение всех пользователей из базы данных"""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT id, telegram_id, chat_id, username, first_name, last_name, language_code, created_at, updated_at FROM users;")
        users = cursor.fetchall()
        
        # Получаем названия колонок
        colnames = ["id", "telegram_id", "chat_id", "username", "first_name", "last_name", "language_code", "created_at", "updated_at"]
        
        cursor.close()
        connection.close()
        
        return colnames, users
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None, None

if __name__ == "__main__":
    print("Получение данных о пользователях...")
    colnames, users = get_users()
    
    if colnames and users is not None:
        # Выводим названия колонок
        print("\t".join(colnames))
        print("-" * 50)
        
        # Выводим данные пользователей
        for user in users:
            print("\t".join(str(field) for field in user))
        
        print(f"\nВсего пользователей: {len(users)}")
    else:
        print("Не удалось получить данные о пользователях.")