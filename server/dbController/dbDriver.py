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
import random
from dbController.loadDefault import fill_tables_with_default_if_they_are_empty, create_default_tables

MODE = "debug"

class dbController():
    def __init__(self, path_to_default_tasks="tasks_sample.csv"):
        self.connection = psycopg2.connect(
            dbname="app_db",#"test_db",
            user="postgres",#"testuser",
            password="postgres",#"testpassword",
            host="db",
            port="5432"
        )
        self.cursor = self.connection.cursor()
        self.passed_ids = []
        create_default_tables(self.cursor)
        fill_tables_with_default_if_they_are_empty(self.cursor, path_to_default_tasks)

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
            "id" : data[0],
            "name" : data[1],
            "email" : data[2],
            "password" : data[3],
            "scores" : {"user_score_grammar" : data[5],
                        "user_score_listenning" : data[6],
                        "user_score_reading_insertion" : data[7],
                        "user_score_reading_skipping" : data[8],
                        "user_score_reading_phoneme" : data[9],
                        "user_score_reading_accent" : data[10],
                        "user_group_id" : data[11],}
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

    def set_task_to_user(self, user_id,task_id):
        self.cursor.execute(set_task_to_user, (user_id,task_id))

        # if task_id not in self.passed_ids:
        #     self.cursor.execute(set_task_to_user, (user_id,task_id))
        #     self.passed_ids.append(task_id)
        # else:
        #     self.cursor.execute(set_task_to_user, (user_id,random.randint(1, 99)))

    def close_task_for_user(self, user_id, task_id):
        self.cursor.execute(detach_task_from_user, (user_id, task_id, ))
        # this was quick bug fix to not getting similar tasks every time
        # if user_id == 1:
        #     self.cursor.execute("DELETE FROM reading_tasks WHERE id = %s;", (task_id, ))
    def set_task_passed_by_user(self, user_id, task_id, result):
        print((user_id, task_id, result, ))
        self.cursor.execute(set_task_to_users_passed_tasks_query, (user_id, task_id, result, ))
        
    def check_if_task_is_passed_by_user(self, user_id, task_id):
        self.cursor.execute(check_if_task_is_passed_by_user, (user_id, task_id))
        cursor_output = self.cursor.fetchone()
        return cursor_output[0] if cursor_output else False
    
    def close_all_tasks_for_user_by_email(self, email):
        self.cursor.execute(detach_all_tasks_from_user_by_email, (email,))


    def update_metrics_for_user_by_email(self, email, user_group_id=None, scores=None):
        
        update_fields = []
        values = []
        if user_group_id:
            update_fields.append("user_group_id = %s")
            values.append(user_group_id)
        if scores:
            for key, value in scores.items():
                update_fields.append(f"{key} = %s")
                values.append(value)
        
        if update_fields:
            values.append(email)
            query = f"""
                UPDATE students 
                SET {', '.join(update_fields)}
                WHERE email = %s
            """
            # print(query)
            # print(email)
            # print(values)
            self.cursor.execute(query, values)
        


    def on_shutdown(self):

        # Close the connection
        self.cursor.close()
        self.connection.close()
    
    def get_all_tasks_types_and_ids(self):
        self.cursor.execute(select_all_tasks_ids_class_difficulty)
        return self.cursor.fetchall()
    
    def get_all_tasks(self):
        self.cursor.execute(select_all_tasks)
        return self.cursor.fetchall()
    
    
    def get_all_users(self):
        self.cursor.execute(select_all_users)
        data = [{
                    "id" : user[0],
                    "name" : user[1],
                    "email" : user[2],
                    "password" : user[3],
                    "scores" : {"user_score_grammar" : user[5],
                                "user_score_listenning" : user[6],
                                "user_score_reading_insertion" : user[7],
                                "user_score_reading_skipping" : user[8],
                                "user_score_reading_phoneme" : user[9],
                                "user_score_reading_accent" : user[10],
                                "user_group_id" : user[11],}
                } for user in self.cursor.fetchall()]
        
        return data
         

    
    def get_errors_of_user_by_email(self, email) -> list: # 
        pass
