import sys
from werkzeug.security import generate_password_hash

def password_hash(password):
    password_hash = generate_password_hash(password)
    print("Hashed password is {}".format(password_hash))

password_hash(sys.argv[1])
