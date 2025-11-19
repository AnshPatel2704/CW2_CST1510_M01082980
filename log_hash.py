import bcrypt


def hash_password(password):
    binery_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(binery_password, salt)
    return hash.decode('utf-8')


def valid_hash(password, hash):
    bin_pwd = password.encode('utf-8')
    bin_hash = hash_password(password).encode('utf-8')
    return bcrypt.checkpw(bin_pwd, bin_hash)

def register_user():
    user_name = input("Enter your username: ")
    user_password = input("Enter your password: ")
    hash = hash_password(user_password)
    with open('user.txt', 'a') as f:
        f.write(f'{user_name},{hash}\n')

def log_in_user():
    user_name = input("Enter your user name: ")
    user_password = input("Enter your password: ")
    with open('user.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        name, hash = user.strip().split(',')

        if user_name == name:
            return valid_hash(user_password, hash)
    return False