from ipaddress import IPv4Network, AddressValueError, NetmaskValueError
import networkmapper
from simple_term_menu import TerminalMenu


class CliMenu:
    def __init__(self):
        self.target_hosts = None
        self.target_ports = None
        self.net_scanner = networkmapper.networkMapper()

    def _network_validation(self, network: str):
        """An internal validation function to check IPv4 validity

        This checks if the user have input a valid IPv4 address with correct CIDR notation

        returns:
            A validated string"""
        try:
            validated_network = IPv4Network(network)
            return str(validated_network)
        except AddressValueError:
            print("Selected network address needs to be 4 octets")
            print("example: 192.168.1.1 or 192.168.1.0/24")
        except NetmaskValueError:
            print("Selected network mask is out of bounds")
            print("Use a netmask of max /32")
        except Exception as e:
            print(f"An unexpected error occured {e}")

    def main_cli(self):
        tools = {
            "INFO": "Go to settings first and set up targets before launching scanners!",
            "Setup": "Change settings for target hosts, ports etc",
            "Network mapper": "Scan networks to find live hosts and open ports",
            "Password cracker": "Crack password hashes with wordlists",
            "Directory buster": "Find hidden subdomains and directories",
            "Login brute force": "Brute forces login for wordpress",
            "Quit": "Exits the program",
        }
        main_menu = TerminalMenu(tools, preview_command=lambda name: tools[name])
        quitting = False
        while not quitting:
            idx = main_menu.show()
            main_menu_choice = list(tools)[idx]  # not the cleanest way
            if main_menu_choice == "Quit":
                quitting = True
            elif main_menu_choice == "Setup":
                self.setup_menu()
            elif main_menu_choice == "Network mapper":
                self.network_mapper_menu()

    def setup_menu(self):
        settings_choices = {
            "Target Hosts": "Sets the target hosts in CIDR notation",
            "Target Ports": "A comma-separated list of ports",
            "Back": "Return to previous menu",
        }
        settings_menu = TerminalMenu(
            settings_choices, preview_command=lambda name: settings_choices[name]
        )
        back = False
        while not back:
            idx = settings_menu.show()
            settings_menu_choice = list(settings_choices)[idx]
            if settings_menu_choice == "Back":
                back = True
            elif settings_menu_choice == "Target Hosts":
                # Asks for IPv4 address, and validates it
                user_input = input("Type a network or host address in CIDR notation: ")
                validated = self._network_validation(network=user_input)
                self.target_hosts = validated
                print(f"The target has been set to: {self.target_hosts}")

    def network_mapper_menu(self):
        scan_alternatives = {
            "ARP-scan": "an explanation",
            "ICMP-scan": "an explanation",
            "TCP-ACK scan": "An explanation",
            "TCP-SYN-scan": "An explanation",
            "Back": "Return to previous menu",
        }
        scanner_menu = TerminalMenu(
            scan_alternatives, preview_command=lambda name: scan_alternatives[name]
        )
        back = False
        while not back:
            idx = scanner_menu.show()
            scanner_menu_choice = list(scan_alternatives)[idx]
            if scanner_menu_choice == "Back":
                back = True


if __name__ == "__main__":
    cli_menu = CliMenu()
    cli_menu.main_cli()
