from database import create_users_table

if __name__ == "__main__":
    print("Проверка подключения к базе данных...")
    if create_users_table():
        print("Подключение успешно! Таблица пользователей создана или уже существует.")
    else:
        print("Ошибка подключения к базе данных.")