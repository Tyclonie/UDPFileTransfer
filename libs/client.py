import os
import socket
from libs import hasher


class Client:
    def wait_for_trust_response(self):
        received, address_from = self.client.recvfrom(1024)
        while address_from != self.server_info:
            print("received data, however its not from the server.")
            received, address_from = self.client.recvfrom(1024)
        return received.decode()

    def ask_to_be_trusted(self, password):
        self.client.sendto(password.encode(), self.server_info)

    def wait_for_data(self):
        received, address_from = self.client.recvfrom(1024)
        while address_from != self.server_info:
            received, address_from = self.client.recvfrom(1024)
        return received.decode()

    def send_data(self, data):
        self.client.sendto(data.encode(), self.server_info)
        
    def create_socket_and_bind(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((socket.gethostbyname(socket.gethostname()), int(input("Enter a port for the client: "))))

    def __init__(self, server_info):
        self.client = None
        self.server_info = server_info


class ClientSideApplicationHandler:
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
            text_response = self.client.wait_for_data()
            if text_response.startswith("*"):
                if text_response == "*handle_setup":
                    self.handle_server_setup()
                    break

    def start_connection(self):
        self.client.ask_to_be_trusted(self.password)
        trusted_response = self.client.wait_for_trust_response()
        while trusted_response == "*wrong_password":
            trusted_response = self.client.wait_for_trust_response() == "*wrong_password"
        if trusted_response == "*accepted":
            print("Interaction authorised.")

    def validate_filesystem(self):
        if "client_data" not in os.listdir(os.getcwd() + "/opt"):
            os.mkdir(os.getcwd() + "/opt/client_data")
        if f"{self.connect_to_information[0]}.txt" not in os.listdir(os.getcwd() + "/opt/client_data/"):
            with open(os.getcwd() + f"/opt/client_data/{self.connect_to_information[0]}.txt", "w") as f:
                f.write("")

    def handle_client_startup(self):
        self.connect_to_information = (input("Enter IP to connect to: "), int(input("Enter server port: ")))
        self.password = input("Enter server password: ")
        self.validate_filesystem()
        self.client = Client(self.connect_to_information)
        self.client.create_socket_and_bind()
        self.start_connection()
        self.maintain_application()

    def __init__(self):
        self.client = None
        self.password = None
        self.connect_to_information = None
        self.handle_client_startup()


if __name__ == "__main__":
    client = Client(("192.168.0.6", 7890))
    client.ask_to_be_trusted(input("Password: "))
    tr = client.wait_for_trust_response()
    while tr == "*wrong_password":
        tr = client.wait_for_trust_response() == "*wrong_password"
    if tr == "*accepted":
        print("Connected")
