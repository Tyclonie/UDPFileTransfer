from libs import server, client, client_setup

class ApplicationHandler:
    def __init__(self):
        self.running_application = None
        self.selected = None
        self.options = ["Server", "Client", "Setup Client To Join Pre-Setup Server"]

    def display_options(self):
        for num in range(len(self.options)):
            print(f"{str(num + 1)} - {self.options[num]}")

    def wait_for_selection(self):
        self.selected = int(input(f"What option would you like to choose? (1 - {len(self.options)}) ")) - 1

    def start_selected_option(self):
        if self.options[self.selected] == "Server":
            self.running_application = server.ServerSideApplicationHandler()
        elif self.options[self.selected] == "Client":
            self.running_application = client.ClientSideApplicationHandler()
        elif self.options[self.selected] == "Setup Client To Join Pre-Setup Server":
            self.running_application = client_setup.ClientSetupHandler()


def main():
    application_handler = ApplicationHandler()
    application_handler.display_options()
    application_handler.wait_for_selection()
    application_handler.start_selected_option()

if __name__ == "__main__":
    main()
