from datetime import datetime
from todo_list_db import sql, db


def create_table_tasks():
    sql.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            start_date TEXT,
            end_date TEXT,
            result INTEGER, 
            user_id INTEGER
        )""")
    db.commit()


def drop_base():
    sql.execute("DROP TABLE tasks")
    db.commit()


def create_user_task(task_text, date_value, user_id):
    task_start_date = datetime.now().strftime('%d-%m-%Y %H:%M')
    if task_start_date < date_value:
        task_end_date = date_value
        task_result = 0
        sql.execute(f"INSERT INTO tasks (text, start_date, end_date, result, user_id) VALUES (?, ?, ?, ?, ?)",
                    (task_text, task_start_date, task_end_date, task_result, user_id))
        db.commit()
    else:
        return 0


def get_user_text(task_id):
    sql.execute(f"SELECT text FROM tasks WHERE id = '{task_id}'")
    return sql.fetchone()[0]


def change_tasks(task_id, new_task):
    sql.execute(f"SELECT id FROM tasks WHERE id = '{task_id}'")

    if sql.fetchone() is None:
        return 0
    else:
        sql.execute(f"UPDATE tasks SET text = '{new_task}' WHERE id = '{task_id}'")
        db.commit()


def change_tasks_date(task_id, new_task_date):
    sql.execute(f"SELECT id FROM tasks WHERE id = '{task_id}'")

    if sql.fetchone() is None:
        return 0
    else:
        sql.execute(f"UPDATE tasks SET end_date = '{new_task_date}' WHERE id = '{task_id}'")
        db.commit()


def get_task_id(text_task):
    sql.execute(f"SELECT id FROM tasks WHERE text = '{text_task}'")
    return sql.fetchone()[0]


def change_tasks_result(task_id):
    sql.execute(f"SELECT id FROM tasks WHERE id = '{task_id}'")

    if sql.fetchone() is None:
        return 0
    else:
        sql.execute(f"UPDATE tasks SET result = '1' WHERE id = '{task_id}'")
        db.commit()


def delete_tasks(task_id):
    sql.execute(f"DELETE FROM tasks WHERE id = '{task_id}'")
    sql.execute(f"UPDATE tasks SET id=id-1 WHERE id > {task_id}")
    db.commit()


def delete_all_tasks(user_id):
    sql.execute(f"DELETE FROM tasks WHERE user_id = '{user_id}'")
    db.commit()


def check_all_tasks(user_id):
    sql.execute(f"SELECT text, start_date, end_date, result FROM tasks WHERE user_id = '{user_id}'")
    return sql.fetchall()


def main():
    create_table_tasks()
    # drop_base()


if __name__ == "__main__":
    main()
