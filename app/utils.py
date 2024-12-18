from passlib.hash import sha256_crypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return sha256_crypt.hash(password)

def verify(plain_password, hashed_password):
    return sha256_crypt.verify(plain_password, hashed_password)  # returns True or False