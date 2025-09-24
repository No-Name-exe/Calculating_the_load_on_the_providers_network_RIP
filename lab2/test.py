import psycopg2

def check_connection():
    try:
        # Установите соединение
        connection = psycopg2.connect(
            database="mydb",
            user="root",
            password="passworddb",
            host="192.168.1.39",
            port="5432"
        )
        # Если соединение успешно, выводим сообщение
        print("Подключение к PostgreSQL успешно!")
        connection.cursor().execute("INSERT INTO public.router (id, title, \"desc\", img) VALUES(1, 'Маршрутизатор провайдера', 'Роутер TP-Link Archer C7 — высокопроизводительный роутер с поддержкой Gigabit Ethernet и мощным процессором', '1.png')")
        connection.commit()

    except Exception as error:
        # Если возникла ошибка, выводим сообщение
        print("Ошибка при подключении к PostgreSQL:", error)

    finally:
        # Закрываем соединение, если оно было открыто
        if 'connection' in locals() and connection:
            connection.close()
            print("Соединение с PostgreSQL закрыто.")

# Вызов функции проверки подключения
check_connection() 