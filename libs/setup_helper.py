import random

class SetupHelper:
    def generate_one_time_password(self):
        for _ in range(6):
            self.one_time_password += str(random.randint(0, 9))

    def __init__(self):
        self.one_time_password = ""
