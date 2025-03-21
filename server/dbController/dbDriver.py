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





conn = psycopg2.connect(
    dbname="test_db",
    user="testuser",
    password="testpassword",
    host="localhost"
)


create_users_table_query = """
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        age INTEGER,
        user_score_grammar INTEGER,
        user_score_listenning INTEGER,
        user_score_reading_insertion INTEGER,
        user_score_reading_skipping INTEGER,
        user_score_reading_phoneme INTEGER,
        user_score_reading_accent INTEGER,
        user_group_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

create_reading_tasks_table_query = """
    CREATE TABLE IF NOT EXISTS reading_tasks (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        text VARCHAR(100) NOT NULL,
        type INTEGER,
        difficulty INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

create_users_tasks_table_query = """
    CREATE TABLE students_tasks (
        students_id INT REFERENCES students(id) ON DELETE CASCADE,
        task_id INT REFERENCES reading_tasks(id) ON DELETE CASCADE,
        enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (students_id, task_id)
    );
    """

select_all_tasks_of_current_user = """
    SELECT task.id, task.name, task.text
    FROM students_tasks
    JOIN students ON students_tasks.students_id = students.id
    JOIN tasks ON users_tasks.course_id = tasks.id
    WHERE students.email = 'test@test.com';
"""

select_user_by_email = """
    SELECT students.id, students.email, students.password
    FROM students
    WHERE students.email = 'test@test.com';
"""

insert_any_user_query = """
    INSERT INTO students (name,\
         email,\
         password,\
         age,\
         user_score_grammar,\
         user_score_listenning,\
         user_score_reading_insertion,\
         user_score_reading_skipping,\
         user_score_reading_phoneme,\
         user_score_reading_accent,\
         user_group_id) 
    SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s 
    WHERE NOT EXISTS (SELECT 1 FROM students);
    """
# WHERE NOT EXISTS (SELECT 1 FROM students)S

cursor = conn.cursor()

# to init only
cursor.execute(create_users_table_query)
cursor.execute(create_reading_tasks_table_query)
cursor.execute(create_users_tasks_table_query)
cursor.execute(insert_any_user_query, ("Andrew", "test@test.com", "test", 20, 70, 80, 70, 70, 70, 70, 0))


cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
    """)


tables = cursor.fetchall()
print("Tables in the database:")



for table in tables:
    print(table[0])

# Close the connection
cursor.close()
conn.close()