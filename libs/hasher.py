import bcrypt


class Hasher:
    def __init__(self):
        self.salt = bcrypt.gensalt(rounds=10)

    def hash_value(self, password):
        return bcrypt.hashpw(password.encode(), self.salt)


if __name__ == "__main__":
    hasher = Hasher()
    print(hasher.hash_value("lolipop"))
