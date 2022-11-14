import os
class CommandLineHandler:
    def __init__(self):
        self.system_name = os.name

    def clear_command_line(self):
        if self.system_name == "nt":
            os.system("cls")
        else:
            os.system("clear")