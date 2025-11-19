from log_hash import hash_password, valid_hash, register_user, log_in_user
def menu():
    print('*'*30)
    print('Welcome to my system')
    print('Choose from the following options: ')
    print('1. Register ')
    print('2. Login')
    print('3. Exit')

def main():
    while True:
        menu()
        choice = input('> ')
        if choice == '1':
            register_user()
        elif choice == '2':
            if log_in_user():
                print('You loged in !!')
            else:
                print('Incorrect log in !!!')
        elif choice == '3':
            print('Good Bye !!')
            break
if __name__ == '__main__':
    main()



import sqlite3

conn = sqlite3.connect('Data/telligence_platform.db')

curr = conn.cursor()

sql = ("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
       )""")

curr.execute(sql)
conn.commit()
conn.close()