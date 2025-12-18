import bcrypt
def generate_hash(psw):
    byte_psw = psw.encode('utf-8')     # str → bytes ✅
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(byte_psw, salt)  # returns bytes ✅
    return hash.decode('utf-8')        # bytes → str ✅


def is_valid_hash(psw, hash):
    hash_ = hash.encode('utf-8')       # str → bytes ✅
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid
