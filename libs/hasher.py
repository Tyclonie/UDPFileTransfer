import bcrypt


class Hasher:
    def __init__(self, salt=None):
        if salt is None:
            self.salt = bcrypt.gensalt(rounds=16)
        else:
            self.salt = salt

    def hash_value(self, password):
        return bcrypt.hashpw(password.encode(), self.salt)


if __name__ == "__main__":
    hasher = Hasher()
    print(hasher.hash_value("lolipop"))
