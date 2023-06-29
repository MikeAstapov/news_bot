import sqlite3


def sql_start():
    global base, cur
    base = sqlite3.connect('lenta.db')
    cur = base.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS lenta_users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE, "
        "user_name TEXT, connect_date, agreement DEFAULT 0)"
    )
    base.commit()


def add_new_user(params):
    user_id = params[0]  # Предполагается, что user_id будет первым элементом в списке params
    cur.execute("SELECT user_id FROM lenta_users WHERE user_id=?", (user_id,))
    existing_user = cur.fetchone()

    if existing_user:
        print(f"Пользователь {user_id} уже существует в базе данных")
    else:
        cur.execute("INSERT INTO lenta_users (user_id, user_name, connect_date, agreement) VALUES(?,?,?,?)", params)
        base.commit()
        print(f"Пользователь {user_id} успешно добавлен в базу данных")


def delete_user_agreement(params):
    cur.execute("UPDATE lenta_users SET agreement = ? where user_id = ?", params)
    base.commit()


def add_user_agreement(params):
    cur.execute("UPDATE lenta_users SET agreement = ? where user_id = ?", params)
    base.commit()


def select_all_users():
    cur.execute("SELECT user_id FROM lenta_users WHERE agreement = 1")
    return cur.fetchall()
