from ipaddress import IPv4Network, AddressValueError, NetmaskValueError
import networkmapper
import passwordcracker
import directorybuster
from simple_term_menu import TerminalMenu


class CliMenu:
    def __init__(self):
        self.target_hosts = None
        self.target_ports = None
        self.target_url = None
        self.hash = None
        self.wordlist = "wordlist/rockyou.txt"
        self.hash_type = None
        self.hash_list = None
        self.net_scanner = networkmapper.NetworkMapper()
        self.password_cracker = passwordcracker.PasswordCracker()
        self.directory_buster = directorybuster.DirectoryBuster()

    def _network_validation(self, network: str) -> str | None:
        """An internal validation function to check IPv4 validity

        This checks if the user have input a valid IPv4 address with correct CIDR notation

        args:
            network (str): Nettwork address as a string

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
        loot_lines = self.password_cracker.cracked
        loot_string = "\n".join(loot_lines)
        return loot_string

    def _loot_dirb(self) -> str:
        """An internal function that displays found password hashes

        This function concatinates all discovered hashes to a string
        with one hash on each line

        returns:
            A multi-line string with discovered hashes"""
        loot_lines = self.directory_buster.loot
        loot_string = "\n".join(loot_lines)
        return loot_string

    def main_cli(self):
        """This displays the main CLI menu

        The main CLI menu with alternatives to all submenus, Information, setup and loot."""

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
            elif main_menu_choice == "Directory buster":
                self.directory_buster_menu()

    def setup_menu(self):
        """Displays the setup menu

        The setup menu is to set up target Hosts, target Ports, wordlists locations and target hashes."""

        settings_choices = {
            "Current Settings": "Press enter to print the current settings",
            "Target URL": "Sets the target URL for web attacks",
            "Target Hosts": "Sets the target hosts in CIDR notation",
            "Target Ports": "A comma-separated list of ports",
            "Hash": "A password hash",
            "Hash Type": "Hash type of hash",
            "Hash list": "Path to a file of hashes",
            "Wordlist": "Path to a wordlist file",
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
            elif settings_menu_choice == "Current Settings":
                print(f"Target Host: {self.target_hosts}")
                print(f"Target Ports: {self.target_ports}")
                print(f"Hash: {self.hash}")
                print(f"Hash Type: {self.hash_type}")
                print(f"Hash List: {self.hash_list}")
                print("\n")
            elif settings_menu_choice == "Target URL":
                # Asks for IPv4 address, and validates it
                user_input = input("Type URL to target website: ")
                self.target_url = user_input
                print(f"The target has been set to: {self.target_url}\n")
            elif settings_menu_choice == "Target Hosts":
                # Asks for IPv4 address, and validates it
                user_input = input("Type a network or host address in CIDR notation: ")
                validated = self._network_validation(network=user_input)
                self.target_hosts = validated
                print(f"The target has been set to: {self.target_hosts}\n")
            elif settings_menu_choice == "Hash":
                user_input = input("Paste the hash to crack: ")
                self.hash = user_input
                print(f"Hash has been set to {self.hash}\n")
            elif settings_menu_choice == "Hash Type":
                user_input = input("Type the hash type (md5, sha1, sha256 etc): ")
                self.hash_type = user_input
                print(f"Hash has been set to {self.hash_type}\n")
            elif settings_menu_choice == "Hash list":
                user_input = input("Enter path to list of hashes: ")
                self.hash_list = user_input
                print(f"Hash has been set to {self.hash_list}\n")
            elif settings_menu_choice == "Wordlist":
                user_input = input("Enter the path wo the wordlist: ")
                self.wordlist = user_input
                print(f"wordlist has been set to {self.hash_list}\n")

    def loot_menu(self):
        """Displays the loot menu

        The loot menu will display any gathered information from performed scans and hash cracking."""

        loot_choices = {
            "Hosts with ports": self._loot_hosts(),
            "Passwords": self._loot_pwd(),
            "Directory buster": self._loot_dirb(),
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
        """Displays the network mapper menu

        The network mapper menu list all possible network scans and performs the scan when selected."""

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
            elif scanner_menu_choice == "ICMP-scan":
                self.net_scanner.ping_network(network=self.target_hosts)
            elif scanner_menu_choice == "TCP-ACK-scan":
                self.net_scanner.tcp_ack(
                    network=self.target_hosts, ports=self.target_ports
                )
            elif scanner_menu_choice == "TCP-SYN-scan":
                self.net_scanner.tcp_syn(
                    network=self.target_hosts, ports=self.target_ports
                )

    def password_cracker_menu(self):
        """Displays the password cracker menu

        the password cracker menu show selected wordlists and perform the hash cracking when selected"""

        pwd_alternatives = {
            "Info!": f"Hash set: {self.hash}\nWordlist: {self.wordlist}\nHash method: {self.hash_type}\nHashlist: {self.hash_list}",
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
                    hash=self.hash,
                    wordlist=self.wordlist,
                    hash_type=self.hash_type,
                    hashlist=self.hash_list,
                )

    def directory_buster_menu(self):
        """Displays the directory bruter menu

        the directory buster menu show selected wordlists and perform the hash cracking when selected"""

        db_alternatives = {
            "Info!": f"Target url: {self.target_url}\nWordlist: {self.wordlist}",
            "Directory bust": "Execute directory busting, requires wordlist and target url set.",
            "Subdirectory bust": "Execute subirectory busting, requires wordlist and target url set.",
            "Back": "Return to previous menu",
        }
        db_menu = TerminalMenu(
            db_alternatives, preview_command=lambda name: db_alternatives[name]
        )
        back = False
        while not back:
            idx = db_menu.show()
            pwd_menu_choice = list(db_alternatives)[idx]
            if pwd_menu_choice == "Back":
                back = True
            elif pwd_menu_choice == "Directory bust":
                self.directory_buster.directory_brute(
                    target=self.target_url, wordlist=self.wordlist
                )


if __name__ == "__main__":
    cli_menu = CliMenu()
    cli_menu.main_cli()
