from ipaddress import IPv4Network, AddressValueError, NetmaskValueError
import networkmapper
import passwordcracker
from simple_term_menu import TerminalMenu


class CliMenu:
    def __init__(self):
        self.target_hosts = None
        self.target_ports = None
        self.hash = "c55f43e33481bbece1d8ec015e406a1e"
        self.wordlist = "wordlist/rockyou.txt"
        self.hash_type = "md5"
        self.net_scanner = networkmapper.networkMapper()
        self.password_cracker = passwordcracker.PasswordCracker()

    def _network_validation(self, network: str) -> str | None:
        """An internal validation function to check IPv4 validity

        This checks if the user have input a valid IPv4 address with correct CIDR notation

        returns:
            A validated IPv4 address as a string, or None if validation failed"""
        try:
            validated_network = IPv4Network(network)
            return str(validated_network)
        except AddressValueError:
            print("Selected network address needs to be 4 octets")
            print("example: 192.168.1.1 or 192.168.1.0/24")
            return None
        except NetmaskValueError:
            print("Selected network mask is out of bounds")
            print("Use a netmask of max /32")
            return None
        except Exception as e:
            print(f"An unexpected error occured {e}")
            return None

    def _loot_hosts(self) -> str:
        """An internal function that displays found hosts

        This function concatinates all discovered hosts to a string
        with one host on each line

        returns:
            A multi-line string with discovered hosts"""
        loot_lines = []
        for host in self.net_scanner.live_hosts.values():
            loot_lines.append(f"IP: {host.ip} - MAC: {host.mac}, ports: {host.ports}")
        loot_string = "\n".join(loot_lines)
        return loot_string

    def _loot_pwd(self) -> str:
        """An internal function that displays found password hashes

        This function concatinates all discovered hashes to a string
        with one hash on each line

        returns:
            A multi-line string with discovered hashes"""
        loot_lines = []
        for pwd in self.password_cracker.cracked:
            loot_lines.append(f"hash: {pwd[0]}, password: {pwd[1]}")
        loot_string = "\n".join(loot_lines)
        return loot_string

    def main_cli(self):
        tools = {
            "INFO": "Go to settings first  and set up targets before launching scanners!",
            "Setup": "Change settings for target hosts, ports etc",
            "Loot": "Displays the hosts and passwords that have been discovered",
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
            elif main_menu_choice == "Loot":
                self.loot_menu()
            elif main_menu_choice == "Network mapper":
                self.network_mapper_menu()
            elif main_menu_choice == "Password cracker":
                self.password_cracker_menu()

    def setup_menu(self):
        settings_choices = {
            "Current Settings": f"Target Hosts: {self.target_hosts}\nTarget ports: {self.target_ports}",
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

    def loot_menu(self):
        loot_choices = {
            "Hosts with ports": self._loot_hosts(),
            "Passwords": self._loot_pwd(),
            "Back": "Return to previous menu",
        }
        loot_menu_object = TerminalMenu(
            loot_choices, preview_command=lambda name: loot_choices[name]
        )
        back = False
        while not back:
            idx = loot_menu_object.show()
            loot_menu_choice = list(loot_choices)[idx]
            if loot_menu_choice == "Back":
                back = True

    def network_mapper_menu(self):
        scan_alternatives = {
            "ARP-scan": "Scans local network using ARP packets \n Requires target network set",
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
            elif scanner_menu_choice == "ARP-scan":
                # TODO: Validate that self.target_hosts have been set!
                self.net_scanner.arp_scan(network=self.target_hosts)

    def password_cracker_menu(self):
        pwd_alternatives = {
            "Info!": f"Hash set: {self.hash}\nWordlist: {self.wordlist}\nHash method: {self.hash_type}",
            "Crack hash": "Execute hash cracking, requires wordlist and hash set.",
            "Back": "Return to previous menu",
        }
        pwd_menu = TerminalMenu(
            pwd_alternatives, preview_command=lambda name: pwd_alternatives[name]
        )
        back = False
        while not back:
            idx = pwd_menu.show()
            pwd_menu_choice = list(pwd_alternatives)[idx]
            if pwd_menu_choice == "Back":
                back = True
            elif pwd_menu_choice == "Crack hash":
                # TODO: Validate that self.target_hosts have been set!
                self.password_cracker.hash_cracker(
                    hash=self.hash, wordlist=self.wordlist, hash_type=self.hash_type
                )


if __name__ == "__main__":
    cli_menu = CliMenu()
    cli_menu.main_cli()
