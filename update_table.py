import psycopg2
from database import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def add_chat_id_column():
    """Добавление поля chat_id в таблицу users"""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Проверяем, существует ли уже поле chat_id
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='chat_id';
        """)
        
        if cursor.fetchone() is None:
            # Добавляем поле chat_id
            cursor.execute("ALTER TABLE users ADD COLUMN chat_id BIGINT;")
            print("Поле chat_id успешно добавлено в таблицу users")
        else:
            print("Поле chat_id уже существует в таблице users")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return True
    except Exception as e:
        print(f"Ошибка при добавлении поля chat_id: {e}")
        return False

if __name__ == "__main__":
    print("Добавление поля chat_id в таблицу users...")
    if add_chat_id_column():
        print("Готово!")
    else:
        print("Ошибка!")