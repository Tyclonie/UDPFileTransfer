import os

class ClientSetupHandler:
    def save_to_file(self):
        if "opt" not in os.listdir(os.getcwd()):
            os.mkdir("opt")
        if "client_data" not in os.listdir(os.getcwd() + "/opt"):
            os.mkdir(os.getcwd() + "/opt/client_data")
        with open(os.getcwd() + f"/opt/client_data/{self.server_ip}.txt", "w") as f:
            f.write(self.salt)

    def __init__(self):
        self.salt = input("Please Enter The Salt: ")
        self.server_ip = input("Please Enter The Server IP: ")
        self.save_to_file()
