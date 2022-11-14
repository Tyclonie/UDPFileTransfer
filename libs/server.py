import os
import socket
import requests
from libs import setup_helper, cli_handler
from colorama import Fore


class Server:
    def wait_for_data(self):
        received, address_from = self.server.recvfrom(1024)
        while address_from != self.client:
            print("received data, however its not from the client.")
            received, address_from = self.server.recvfrom(1024)
        return received.decode()

    def send_data(self, data):
        self.server.sendto(data.encode(), self.client)

    def set_client(self, client_info):
        self.server.sendto("*accepted".encode(), client_info)
        self.client = client_info

    def handle_setup_connection(self):
        self.server.sendto("*handle_setup".encode(), self.client)

    def wait_for_setup_connection(self, handler):
        received, address_from = self.server.recvfrom(1024)
        while received.decode() != str(handler.setup_helper.one_time_password):
            self.server.sendto("*wrong_password".encode(), address_from)
            received, address_from = self.server.recvfrom(1024)
        handler.received_data = (received, address_from)

    def wait_for_connection_attempt(self, handler, password):
        received, address_from = self.server.recvfrom(1024)
        while received != password:
            self.server.sendto("*wrong_password".encode(), address_from)
            received, address_from = self.server.recvfrom(1024)
        handler.received_data = (received, address_from)

    def create_socket_and_bind(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()), self.port))

    def __init__(self, port):
        self.server = None
        self.client = None
        self.port = port


class ServerSideApplicationHandler:
    def handle_setup(self):
        self.setup_helper = setup_helper.SetupHelper()
        print(f"""Welcome to the server setup. To complete the setup you will be required to connect with a client.
To connect for the first time you will be given a one time password shortly. {Fore.RED}WARNING:{Fore.RESET} Do NOT 
share the one time password with anyone!{Fore.RESET}""")
        self.server = Server(int(input("What port would you like to use? ")))
        self.command_line_handler.clear_command_line()
        self.setup_helper.generate_one_time_password()
        print(f"""Please connect using a client with public IP address: {requests.get("https://api.ipify.org").text}  
If you would like to connect locally, use IP address: {socket.gethostbyname(socket.gethostname())}
Using port: {str(self.server.port)}
Your one time password is: {Fore.GREEN}{self.setup_helper.one_time_password}{Fore.RESET}""")
        self.server.create_socket_and_bind()
        self.server.wait_for_setup_connection(self)
        self.server.set_client(self.received_data[1])
        print(f"Client connected: {self.received_data[1]}")
        self.server.handle_setup_connection()
        data = self.server.wait_for_data()
        while not data.startswith("*set_password"):
            data = self.server.wait_for_data()
        password = data[14:].encode()
        with open(os.getcwd() + "/opt/server_configuration.txt", "wb") as f:
            f.write(password)
        print("Setup complete")
        self.server.send_data("*setup_complete")

    def handle_download(self, filename):
        with open(self.cwd + filename, "rb") as f:
            data = f.read()
        num_of_bytes = len(data)
        num_of_packs = num_of_bytes // 128
        if num_of_bytes % 128 != 0:
            num_of_packs += 1
        self.server.send_data(f"{filename[-filename[::-1].index('.'):]} {str(num_of_packs)}")
        for x in range(num_of_packs):
            try:
                print(str([str(x), data[128 * x:128 * (x + 1) - 1]]))
                self.server.send_data(str([str(x), data[128 * x:128 * (x + 1) - 1]]))
            except IndexError:
                self.server.send_data(str([str(x), data[128 * (num_of_packs - 1):]]))

    def maintain_server(self):
        while True:
            received = self.server.wait_for_data()
            if received.startswith("*"):
                if received.startswith("*load_dir"):
                    pass
                elif received.startswith("*download"):
                    self.handle_download(received[12:])

    def handle_server_startup(self):
        self.server = Server(int(input("Enter port for the server: ")))
        self.server.create_socket_and_bind()
        self.command_line_handler.clear_command_line()
        print(f"""Please connect using a client with public IP address: {requests.get("https://api.ipify.org").text}  
If you would like to connect locally, use IP address: {socket.gethostbyname(socket.gethostname())}
Using port: {str(self.server.port)}""")
        with open(os.getcwd() + "/opt/server_configuration.txt", "rb") as f:
            password = f.read()
        self.server.wait_for_connection_attempt(self, password)
        self.server.set_client(self.received_data[1])
        print(f"Client connected: {self.received_data[1]}")
        self.server.send_data(f"*load {str(os.listdir(self.cwd))}")
        self.maintain_server()

    def __init__(self):
        self.cwd = "C://"
        self.received_data = (None, None)
        self.server = None
        self.setup_helper = None
        self.command_line_handler = cli_handler.CommandLineHandler()
        self.command_line_handler.clear_command_line()
        if "server_configuration.txt" not in os.listdir(os.getcwd() + "/opt"):
            self.handle_setup()
        else:
            self.handle_server_startup()


if __name__ == "__main__":
    ServerSideApplicationHandler()
