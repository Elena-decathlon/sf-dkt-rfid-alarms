import sys
from werkzeug.security import generate_password_hash

def pass_hash(password):
    hashed_pwd = generate_password_hash(password, 'sha256')
    print("Hashed password is {}".format(hashed_pwd))

pass_hash(sys.argv[1])
