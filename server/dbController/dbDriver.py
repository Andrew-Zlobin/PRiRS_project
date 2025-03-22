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
# и фигачим сюда все права GRANT ALL insert_any_user_queryPRIVILEGES ON DATABASE test_db TO testuser;

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



# WHERE NOT EXISTS (SELECT 1 FROM students)S

cursor = conn.cursor()

# to init only


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