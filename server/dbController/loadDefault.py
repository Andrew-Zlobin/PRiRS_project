from queries import create_users_table_query, \
                    create_reading_tasks_table_query, \
                    create_users_tasks_table_query, \
                    insert_any_user_query

def create_default tables(cursor, ):
    cursor.execute(create_users_table_query)
    cursor.execute(create_reading_tasks_table_query)
    cursor.execute(create_users_tasks_table_query)
    cursor.execute(insert_any_user_query, ("Andrew", "test@test.com", "test", 20, 70, 80, 70, 70, 70, 70, 0))

