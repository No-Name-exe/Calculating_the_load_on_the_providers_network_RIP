import psycopg2

conn = psycopg2.connect(dbname="mydb", host="192.168.1.25", user="root", password="passworddb", port="5432")

cursor = conn.cursor()
 
# cursor.execute("INSERT INTO public.phenomen (id, title, desc, img) VALUES(1, 'Маршрутизатор провайдера', 'Роутер TP-Link Archer C7 — высокопроизводительный роутер с поддержкой Gigabit Ethernet и мощным процессором', '1.png')")

 
conn.commit()   # реальное выполнение команд sql1
 
cursor.close()
conn.close()