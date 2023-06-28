import sqlite3

def sql_start():
    global base, cur
    base = sqlite3.connect('database/lenta.db')
    cur = base.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS lenta_users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id , user_name TEXT, connect_date, agreement)"
    )
    base.commit()

def add_new_user(params):
    cur.execute("INSERT INTO lenta_users (user_id, user_name, connect_date, agreement) VALUES(?,?,?,?)", params)
    base.commit()