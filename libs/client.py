import os
import socket
from libs import hasher, cli_handler, utilites


class Client:
    def wait_for_trust_response(self):
        received, address_from = self.client.recvfrom(1024)
        while address_from != self.server_info:
            received, address_from = self.client.recvfrom(1024)
        return received.decode()

    def ask_to_be_trusted(self, password):
        self.client.sendto(password.encode(), self.server_info)

    def wait_for_data(self):
        received, address_from = self.client.recvfrom(1024)
        while address_from != self.server_info:
            received, address_from = self.client.recvfrom(1024)
        return received.decode()

    def wait_for_data_no_decode(self):
        received, address_from = self.client.recvfrom(1024)
        while address_from != self.server_info:
            received, address_from = self.client.recvfrom(1024)
        return received

    def send_data(self, data):
        self.client.sendto(data.encode(), self.server_info)
        
    def create_socket_and_bind(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((socket.gethostbyname(socket.gethostname()), int(input("Enter a port for the client: "))))

    def __init__(self, server_info):
        self.client = None
        self.server_info = server_info


class ClientSideApplicationHandler:
    def update_command_line(self, listed_directory):
        self.command_line_handler.clear_command_line()
        for item in listed_directory:
            print(item)
        print("\ncd [dir] - Change dir, '..' to go back | copy [file/dir] - Copy specified file/folder")

    def handle_server_setup(self):
        hash_maker = hasher.Hasher()
        hashed_password = hash_maker.hash_value(input("What would you like to set the server password to?: ")).decode()
        with open(os.getcwd() + f"/opt/client_data/{self.connect_to_information[0]}.txt", "wb") as f:
            f.write(hash_maker.salt)
        self.client.send_data(f"*set_password {hashed_password}")
        if self.client.wait_for_data() == "*setup_complete":
            print("Setup complete")

    def maintain_application(self):
        while True:
            # HANDLE COMMANDS FROM SERVER
            text_response = self.client.wait_for_data()
            if text_response.startswith("*"):
                if text_response.startswith("*handle_setup"):
                    self.handle_server_setup()
                    break
                elif text_response.startswith("*load"):
                    self.update_command_line(utilites.rebuild_list(text_response[6:]))
            # HANDLE COMMANDS TO SERVER
            what_to_do_now = input("Enter command: ")
            while not what_to_do_now.startswith("cd") and not what_to_do_now.startswith("copy"):
                what_to_do_now = input("Enter valid command: ")
            if what_to_do_now.startswith("cd"):
                self.client.send_data(f"*load_dir {what_to_do_now[3:]}")
            elif what_to_do_now.startswith("copy"):
                file_to_copy = what_to_do_now[5:]
                self.client.send_data(f"*download {file_to_copy}")
                total_num_of_packs = int(self.client.wait_for_data())
                sorted_packs = [None] * total_num_of_packs
                for _ in range(total_num_of_packs):
                    bytes_received = self.client.wait_for_data_no_decode()[::-1]
                    pack_data = bytes_received[bytes_received.index(b" | ") + 3:][::-1]
                    pack_num = bytes_received[:bytes_received.index(b" | ")][::-1]
                    sorted_packs[int(pack_num.decode())] = pack_data
                bytes_to_write = b""
                for pack in sorted_packs:
                    bytes_to_write += pack
                with open(os.getcwd() + f"/{file_to_copy}", "wb") as f:
                    f.write(bytes_to_write)

    def start_connection(self):
        self.client.ask_to_be_trusted(self.password)
        trusted_response = self.client.wait_for_trust_response()
        while trusted_response == "*wrong_password":
            self.password = input("Password entered was incorrect, try again: ")
            self.client.ask_to_be_trusted(self.password)
            trusted_response = self.client.wait_for_trust_response()
        if trusted_response == "*accepted":
            print("Interaction authorised.")

    def validate_filesystem(self):
        if "opt" not in os.listdir(os.getcwd()):
            os.mkdir(os.getcwd() + "/opt")
        if "client_data" not in os.listdir(os.getcwd() + "/opt"):
            os.mkdir(os.getcwd() + "/opt/client_data")
        if f"{self.connect_to_information[0]}.txt" not in os.listdir(os.getcwd() + "/opt/client_data/"):
            self.first_time = True
            with open(os.getcwd() + f"/opt/client_data/{self.connect_to_information[0]}.txt", "w") as f:
                f.write("")

    def handle_client_startup(self):
        self.connect_to_information = (input("Enter IP to connect to: "), int(input("Enter server port: ")))
        self.password = input("Enter server password (or one time password): ")
        self.validate_filesystem()
        if f"{self.connect_to_information[0]}.txt" in os.listdir(os.getcwd() + "/opt/client_data"):
            with open(os.getcwd() + f"/opt/client_data/{self.connect_to_information[0]}.txt", "rb") as f:
                hash_maker = hasher.Hasher(f.read())
            if not self.first_time:
                self.password = hash_maker.hash_value(self.password).decode()
        self.client = Client(self.connect_to_information)
        self.client.create_socket_and_bind()

    def __init__(self):
        self.first_time = False
        self.client = None
        self.password = None
        self.connect_to_information = None
        self.command_line_handler = cli_handler.CommandLineHandler()
        self.handle_client_startup()
        self.start_connection()
        self.maintain_application()


if __name__ == "__main__":
    client = Client(("192.168.0.6", 7890))
    client.ask_to_be_trusted(input("Password: "))
    tr = client.wait_for_trust_response()
    while tr == "*wrong_password":
        tr = client.wait_for_trust_response() == "*wrong_password"
    if tr == "*accepted":
        print("Connected")
