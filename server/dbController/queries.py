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
        type VARCHAR(100) NOT NULL,
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

create_users_passed_tasks_table_query = """
    CREATE TABLE students_passed_tasks (
        students_id INT REFERENCES students(id) ON DELETE CASCADE,
        task_id INT REFERENCES reading_tasks(id) ON DELETE CASCADE,
        success INTEGER,
        enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (students_id, task_id)
    );
    """

select_all_tasks_of_current_user = """
    SELECT rt.* 
    FROM reading_tasks rt
    JOIN students_tasks st ON rt.id = st.task_id
    JOIN students s ON st.students_id = s.id
    WHERE s.email = %s
    ORDER BY st.enrolled_at ASC
"""
# select_all_tasks_of_current_user = """
#     SELECT reading_tasks.id, reading_tasks.name, reading_tasks.text
#     FROM students_tasks
#     JOIN students ON students_tasks.students_id = students.id
#     JOIN reading_tasks ON students_tasks.task_id = reading_tasks.id
#     WHERE students.email = "test@test.com";
# """

select_user_by_email = """
    SELECT *
    FROM students
    WHERE students.email = %s;
"""

select_all_tasks_ids_class_difficulty = """
    select reading_tasks.id, reading_tasks.type, reading_tasks.difficulty
    from reading_tasks
"""

select_all_tasks = """
    select *
    from reading_tasks
"""

select_all_users = """
    SELECT *
    FROM students;
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

insert_user_query = """
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
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
"""

insert_task_query = """
    INSERT INTO reading_tasks (name, text, type, difficulty)
    VALUES 
        (%s, %s, %s, %s);

"""

# это пиздец ребят, надо переписать. Я бы за такое сам себя бы зазашкварил
count_tasks_query = """
    SELECT COUNT(*) FROM reading_tasks;
"""
# ну тут то же самое
count_users_query = """
    SELECT COUNT(*) FROM students;
"""
count_users_tasks_query = """
    SELECT COUNT(*) FROM students_tasks;
"""

set_task_to_user = """
    INSERT INTO students_tasks (students_id, task_id) 
    VALUES (%s, %s) 
    ON CONFLICT (students_id, task_id) DO NOTHING;
"""

set_task_to_users_passed_tasks_query = """
    INSERT INTO students_passed_tasks (students_id, task_id, success) 
    VALUES (%s, %s, %s) 
    ON CONFLICT (students_id, task_id) DO NOTHING; 
"""

check_if_task_is_passed_by_user = """
   SELECT EXISTS (
                SELECT 1
                FROM students_passed_tasks
                WHERE students_id = %s AND task_id = %s
            );
"""

detach_task_from_user = """
    DELETE FROM students_tasks WHERE students_id = %s AND task_id = %s
"""

detach_task_from_user_by_email = """
    DELETE FROM students_tasks
    WHERE students_id = (
        SELECT id FROM students WHERE email = 'student@example.com'
    )
    AND task_id = 123;
"""

detach_all_tasks_from_user_by_email = """
    DELETE FROM students_tasks
    WHERE students_id = (
        SELECT id FROM students WHERE email = %s
    );
"""
