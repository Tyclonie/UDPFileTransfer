import bcrypt


class Hasher:
    def __init__(self):
        self.salt = bcrypt.gensalt()

    def digest(self, string):
        self.hasher = hashlib.sha512(string.encode())
        return self.hasher.hexdigest()


if __name__ == "__main__":
    hasher = Hasher()
    print(hasher.digest("lol"))
