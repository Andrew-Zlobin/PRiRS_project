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