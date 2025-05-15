from dbController.queries import *
from dbController.dbInstancies import *
import pandas as pd
from random import choices

def create_default_tables(cursor):
    cursor.execute(create_users_table_query)
    cursor.execute(create_reading_tasks_table_query)
    cursor.execute(create_users_tasks_table_query)
    cursor.execute(create_users_passed_tasks_table_query)
    # cursor.execute(insert_any_user_query, ("Andrew", "test@test.com", "test", 20, 70, 80, 70, 70, 70, 70, 0))

def fill_tables_with_default_if_they_are_empty(cursor, path_to_tasks):
    cursor.execute(count_tasks_query)
    users_counter = cursor.fetchone()[0]
    if users_counter < 90:
        cursor.execute(insert_any_user_query, ("Andrew", "test@test.com", "test", 20, 70, 60, 50, 40, 40, 40, 0))
        for _ in range(100):
            new_user = User()
            
            cursor.execute(insert_user_query, 
                           (new_user.name, 
                            new_user.email, 
                            new_user.password, 
                            new_user.age,
                            new_user.scores[scores_keys_template[0]],
                            new_user.scores[scores_keys_template[1]],
                            new_user.scores[scores_keys_template[2]],
                            new_user.scores[scores_keys_template[3]],
                            new_user.scores[scores_keys_template[4]],
                            new_user.scores[scores_keys_template[5]],
                            1))
   
    cursor.execute(count_tasks_query)
    tasks_counter = cursor.fetchone()[0]
    if tasks_counter < 90:
        tasks = pd.read_csv(path_to_tasks)
        tasks_to_insert = [(row["Name"], row["Text"], row["Type"], row["difficulty"]) for index, row in tasks.iterrows()]
        # print(tasks_to_insert[:5])
        cursor.executemany(insert_task_query, tasks_to_insert)
    
    cursor.execute(count_users_tasks_query)
    users_tasks_counter = cursor.fetchone()[0]
    if users_tasks_counter < 90:
        cursor.execute("SELECT * FROM students;")  # Change 'users' to your actual table name
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM reading_tasks;")
        tasks = cursor.fetchall()

        for user in users:
            # print("last one", choices(tasks, k=10)[0][0])
            for task in choices(tasks, k=10):
                # print(user[0],task[0])
                cursor.execute(set_task_to_user, (user[0],task[0]))
    cursor.execute(select_all_tasks_of_current_user, ('test@test.com',))
#     cursor.execute("""
#     SELECT rt.* 
#     FROM reading_tasks rt
#     JOIN students_tasks st ON rt.id = st.task_id
#     JOIN students s ON st.students_id = s.id
#     WHERE s.email = %s
# """, ('example@email.com',))
    # print(cursor.fetchall())
