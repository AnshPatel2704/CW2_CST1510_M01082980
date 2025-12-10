import sqlite3
import pandas as pd

def create_user_table(conn):
    curr = conn.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
    """
    curr.execute(sql)
    conn.commit()

def add_user(conn, name, hash_password):
    curr = conn.cursor()
    sql = "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)"
    curr.execute(sql, (name, hash_password))
    conn.commit()

def migrate_user_data():
    with open("DATA/user.txt", 'r') as f:
        users = f.readlines()
        print(users)

    for user in users:
        name, hash = user.strip().split(',')
        add_user(conn, name, hash)

def get_all_users(conn):
    curr = conn.cursor()
    sql = "SELECT * from users"
    curr.execute(sql)
    users = curr.fetchall()
    conn.close()
    return(users)


def get_user(name_):
    curr = conn.cursor()
    sql = "SELECT * from users WHERE username = ?"
    param = (name_,)
    curr.execute(sql,param)
    user = curr.fetchone()
    conn.close()
    return(user)

conn = sqlite3.connect(r'DATA/intelligence_platform.db')
data = pd.read_csv('DATA\datasets_metadata.csv')
data.to_sql











'''
create_user_table(conn)

with open('DATA/user.txt', 'r') as f:
    users = f.readlines()

for user in users:
    name, hash_password = user.strip().split(',')
    add_user(conn, name, hash_password)

conn.close()'''