import bcrypt

def hash_password(password):

    """Ein eingegebenes Passwort wird verschlüsselt."""

    password_bytes = password.encode("utf-8") # in bytes umwandeln
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8") #str

def check_password(password, hashed_password):

    """Ein eingegebenes Passwort wird mit dem verschlüsselten Passwort auf Gleichheit getestet."""

    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes) #bool

if __name__ == "__main__":
    p= "1234"
    h = bcrypt.hashpw(p.encode("utf-8"), bcrypt.gensalt())
    print(h.decode("utf-8"))
    print(check_password(p , h.decode("utf-8")))