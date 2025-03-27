import psycopg2

# теперь буду писать комменты на русском, потому что я заебался


# Итак, небольшой квикстарт в постгресс для быдла:
# Установ очка: sudo apt install postgresql postgresql-contrib
# Смотрим не наебнулся ли сервайс: sudo systemctl status postgresql
# Стартуем дефолтного юзера: sudo -i -u postgres
# Стартуем модный (как говно слона) шелл для управления постгресом: psql
#     сразу пояснение: шелл закрывается на \q
#     сразу ещё одно пояснение выход из пользователя exit
# в шелле фигачим новый пароль ALTER USER postgres PASSWORD '07072002';
# и начинаем редачить вот эту хуйню (со своего обычного юзера): sudo vim /etc/postgresql/17/main/postgresql.conf
#     меняем listen_addresses = '*'
# теперь тут sudo vim /etc/postgresql/17/main/pg_hba.conf
#     вставляем host    all             all             0.0.0.0/0               md5
# и перезапускаем сервайс sudo systemctl restart postgresql


# далее в psql ебашим вот это (куда потом будем подключаться) CREATE DATABASE test_db;
# то же самое для пользователя: CREATE USER testuser WITH ENCRYPTED PASSWORD 'testpassword';
# и фигачим сюда все права GRANT ALL PRIVILEGES ON DATABASE test_db TO testuser;

# УПД БЛЕАТЬ
# пришлось насвинячить ещё сильнее, выполнив:

# GRANT USAGE ON SCHEMA public TO your_username;
# GRANT CREATE ON SCHEMA public TO your_username;
# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;
# ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO your_username;


# делать так ни в коем случае нельзя, но для демки которая только на локалхосте существует - съедобно


# ну и раз уж тут туториалы пишем, для работы одной из штук в построении транкрипции нужна ffmpeg, поэтому не забываем
# sudo apt install ffmpeg

from dbController.queries import *

from dbController.loadDefault import fill_tables_with_default_if_they_are_empty, create_default_tables

MODE = "debug"

class dbController():
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="test_db",
            user="testuser",
            password="testpassword",
            host="localhost"
        )
        self.cursor = self.connection.cursor()
        create_default_tables(self.cursor)
        fill_tables_with_default_if_they_are_empty(self.cursor)

        # self.cursor.execute("""
        #         SELECT table_name FROM information_schema.tables
        #         WHERE table_schema = 'public'
        #     """)


        # tables = self.cursor.fetchall()
        # print("Tables in the database:")



        # for table in tables:
        #     print(table[0])

    def get_user(self, email):
        self.cursor.execute(select_user_by_email, (email, ))
        data = self.cursor.fetchall()[0]
        # print("user data : ", data)
        user = {
            "name" : data[1],
            "email" : data[2],
            "password" : data[3]
            }
        return user
    def get_task_for_user(self, email):
        self.cursor.execute(select_all_tasks_of_current_user, (email, ))
        return [{
                "key": task[0],
                "name": task[1],
                "text": task[2],
                "difficulty": task[4]}
                    for task in self.cursor.fetchall()]

    def on_shutdown(self):

        # Close the connection
        self.cursor.close()
        self.connection.close()