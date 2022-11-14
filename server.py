import os
import socket
import libs.hasher


class Application:
    def __init__(self):
        if "server_configuration.json" not in os.listdir():
            with open("server_configuration.json", "w") as f:
                f.write("{\"password\": \"" + libs.hasher.Hasher().digest(input("Set A Password: ")) + "\"}")


if __name__ == "__main__":
    Application()
