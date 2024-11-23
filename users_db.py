from todo_list_db import sql, db


def create_table_users():
    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT,
        password TEXT
    )""")
    db.commit()


def drop_base():
    sql.execute("DROP TABLE users")
    db.commit()


def check_user(user_login, user_password):
    sql.execute(f"SELECT id FROM users WHERE login = '{user_login}' AND password = '{user_password}'")
    if sql.fetchone() is None:
        return 0
    else:
        sql.execute(f"SELECT id FROM users WHERE login = '{user_login}' AND password = '{user_password}'")
        user_id = sql.fetchone()[0]
        if get_password(user_id, user_password) is None:
            return 0
        else:
            return 1


def create_user(user_login, user_password):
    sql.execute(f"SELECT id FROM users WHERE login = '{user_login}'")

    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users (login, password) VALUES (?, ?)", (user_login, user_password))
        db.commit()
    return get_user(user_login)


def get_user(login):
    sql.execute(f"SELECT id, login FROM users WHERE login = '{login}'")
    return sql.fetchone()


def get_password(user_id, user_password):
    sql.execute(f"SELECT password FROM users WHERE id = '{user_id}' AND password = '{user_password}'")
    return sql.fetchone()


def change_password(user_id, user_password, new_password):
    sql.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
    if sql.fetchone() is None:
        return 0
    else:
        if get_password(user_id, user_password) is None:
            return 0
        else:
            sql.execute(f"UPDATE users SET password = '{new_password}' WHERE id = '{user_id}'")
            db.commit()


def delete_user(user_id):
    sql.execute(f"DELETE FROM users WHERE id = '{user_id}'")
    sql.execute(f"UPDATE users SET id=id-1 WHERE id > {user_id}")
    db.commit()


def main():
    create_table_users()
    #drop_base()


if __name__ == "__main__":
    main()
