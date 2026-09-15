from dataclasses import dataclass, field
from ipaddress import IPv4Network, AddressValueError, NetmaskValueError
import random
from scapy.all import srp, Ether, ARP, ICMP, IP, sr, sr1, TCP, send


@dataclass
class Host:
    ip: str
    mac: str = ""
    ports: list[int] = field(default_factory=list)
    live: bool = True

    def add_ports(self, new_ports):
        self.ports = sorted(set(self.ports) | set(new_ports))


class networkMapper:
    def __init__(self, network: str = "192.168.1.0/24", timeout: float = 2.0):
        self.network = IPv4Network(network)
        self.timeout = timeout
        self.live_hosts = {}

    def _network_validation(self, network: str) -> IPv4Network | None:
        """An internal validation function to check IPv4 validity

        This checks if the user have input a valid IPv4 address with correct CIDR notation

        args:
            network (str): Nettwork address as a string

        returns:
            A validated IPv4 address as a string, or None if validation failed"""
        try:
            validated_network = IPv4Network(network)
            return validated_network
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

    def _validate_ports(self, ports: str) -> int | list[int] | tuple:
        """An internal validation function to validate ports

        This function takes a string and converts it to either an int, a list of int or a tuple
        single int for one port, list of int for multiple ports and a tuple for a port range

        args:
            ports (str): A string with the port values

        returns:
            int: for a single port
            list[int]: for multiple ports
            tuple: for a port range"""
        result = []
        try:
            if "-" in ports:
                split = ports.split("-")
                result = int(split[0]), int(split[1])
                if result[0] > result[1]:
                    raise ValueError("Port range must go from lowest to highest")
            elif "," in ports:
                split = ports.split(",")
                for i in split:
                    result.append(int(i))
            else:
                print(ports)
                result = int(ports)
        except ValueError as e:
            print(f"Invalid port number selected: {e}")
        return result

    def add_host(
        self,
        ip: str,
        mac: str | None = None,
        ports: list[int] | None = None,
        live: bool = True,
    ):
        """An internal helper function

        This function adds hosts to object variable to store discovered hosts and ports


        Args:
            ip (str): An IP address of the host
            mac (str): The MAC address of the host
            ports (list[int]): A list of port numbers
            live (bool): A True or False to indicate if the host is live


        """
        if ip in self.live_hosts:
            host = self.live_hosts[ip]
            if ports:
                host.add_ports(ports)
            if mac:
                host.mac = mac
            host.live = live
        else:
            self.live_hosts[ip] = Host(
                ip=ip, mac=mac or "", ports=ports or [], live=live
            )

    # layer 2 scan
    def arp_scan(self, network: str | None = None) -> list[dict]:
        """Performs an ARP scan on local subnet to discover Host IPs and their MAC addresses

        This scan only works on local subnet (Layer 2) and is not able to traverse to another subnet.
        An intervall of 0.05 seconds have been chosen to allow for wifi connected devices to respond,
        and not falesly show up as non-responsive.

        Args:
            network (str|None): A string with CIDR network address

        returns:
            A list of dicts containing the IP addresses and MAC addresses of responsive and live hosts"""
        if network is None:
            network = str(self.network)
        results = []
        try:
            ans, _ = srp(
                Ether(
                    dst="ff:ff:ff:ff:ff:ff"
                )  # using all ff sends the packet to broadcast
                / ARP(pdst=network),
                timeout=2,
                inter=0.05,  # Added intervall to allow for WiFi clients to respond.
            )
            for _, r in ans:
                self.add_host(r.psrc, mac=r.hwsrc)
                results.append(self.live_hosts[r.psrc])
                print(f"Added to loot: {r.psrc}")
        except PermissionError as e:
            print(f"This must be run as Admin/root {e}")
        return results

    # This uses sr and nor sr1 - fires ALL pings at once = noisy noisy!
    # Layer 3 scan
    def ping_network_fast(self, network: str | None = None) -> list[dict]:
        """Performs an ICMP scan og selected network to find live hosts

        This scan operates on Layer 3 and can be routed to selected network. By using the sr module
        this sends all ICMP packets at once and is very noisy!

        Args:
            network (str|None): A string with CIDR network address

        returns:
            A list of dictionaries displaying the IP address of responsive hosts."""
        if network == None:
            network = str(self.network)
        results = []
        try:
            ans, _ = sr(
                IP(dst=network) / ICMP(),
                timeout=2,
                verbose=0,
            )
            for _, r in ans:
                self.add_host(r.src)
                results.append(self.live_hosts[r.src])
        except PermissionError as e:
            print(f"This must be run as Admin/root {e}")
        return results

    # this uses the sr1, firing one ping at the time, more stealthy
    # layer 3 scan
    def ping_network(self, network: str | None = None) -> list[dict]:
        """Performs an ICMP scan on selected network to fin live hosts

        This scan operates on Layer 3 and can be routed to selected network. By using the sr1 module
        this sends one ICMP packet at the time for a more stealthy approach.

        Args:
            network (str|None): A string with CIDR network address

        returns:
            A tuple with two lists, one with dicts of live hosts and one with dicts of blocked hosts.
        """
        if network is None:
            addresses = self.network
        else:
            addresses = self._network_validation(network)
            print("checked addresses")
            print(type(addresses))
        results = []
        try:
            for host in addresses:
                if len(list(addresses)) > 1 and host in (
                    addresses.network_address,
                    addresses.broadcast_address,
                ):
                    continue
                ans = sr1(
                    IP(dst=str(host)) / ICMP(),
                    timeout=0.2,  # sets the agressiveness of the scan
                    verbose=0,
                )
                if ans is None:
                    continue
                # Not sure if i want to store blocked ICMPs - deactivated for now
                # elif int(ans.getlayer(ICMP).type) == 3 and int(
                #     ans.getlayer(ICMP).code
                # ) in [  # type 3 is destination unreachable
                #     1,
                #     2,
                #     3,
                #     9,
                #     10,
                #     13,
                # ]:
                # blocking.append({"IP": str(host)})
                else:
                    self.add_host(ans.src)
                    results.append(self.live_hosts[ans.src])
                    print(f"Added to loot: {ans.src}")
        except PermissionError as e:
            print(f"This must be run as Admin/root {e}")
        return results

    # Layer 4 scan with TCP ACK
    def tcp_ack(
        self, network: str | None = None, ports: list[int] | None = None
    ) -> list[dict]:
        """Performs a TCP ACK scan to reveal active hosts on selected network

        This scan sends an ACK packet to selected ports, if there is a service on the selected
        port, a RST packet is returned since we do not have a connection established. This method
        can penetrate stateless firewalls.

        Args:
            network (str|None): A string with CIDR network address
            ports (list[int]|None): A list of int for the port numbers

        returns:
            A list of dicts with the IP and open ports of live hosts."""  ## open ports can't be verified this way
        addresses = self.network
        if ports == None:
            ports = [80]  # Setting port 80 as standard, most likely to get thorugh FW
        results = []
        try:
            for host in addresses:
                if len(list(addresses)) > 1 and host in (
                    addresses.network_address,
                    addresses.broadcast_address,
                ):
                    continue

                for port in ports:
                    src_port = random.randint(1025, 65534)
                    dst_port = port
                    ans = sr1(
                        IP(dst=str(host))
                        / TCP(sport=src_port, dport=dst_port, flags="A"),
                        timeout=2,
                        verbose=0,
                    )
                    # Maybe break after first validated response?
                    if ans is None:
                        continue
                    elif ans.haslayer(TCP) and ans[TCP].flags == "R":
                        self.add_host(ans.src)
                        results.append(self.live_hosts[ans.src])
        except PermissionError as e:
            print(f"This must be run as Admin/root {e}")
        return results

    # Layer 4 scan with TCP syn
    def tcp_syn(
        self, network: str | None = None, ports: list[int] | None = None
    ) -> list[dict]:
        """Performs a TCP SYN scan to reveal active hosts on selected network

        This scan sends an SYN packet to selected ports, if there is a service on the selected
        port, an ACK is recieved if the port is open. If an ACK is received and the port is open
        we close it gracefully with an RST packet. This method can penetrate stateful firewalls.

        Args:
            network (str|None): A string with CIDR network address
            ports (list[int]|None): A list of int for the port numbers

        returns:
            A list of dicts with the IP and open ports of live hosts."""
        addresses = self.network
        if ports == None:
            ports = [80]
        results = []
        try:
            for host in addresses:
                open_ports = []
                closed_ports = []
                filteres_ports = []
                if len(list(addresses)) > 1 and host in (
                    addresses.network_address,
                    addresses.broadcast_address,
                ):
                    continue
                for port in ports:
                    client_seq = random.randint(1000, 10000)
                    server_seq = None
                    src_port = random.randint(1025, 65534)
                    dst_port = port
                    ans = sr1(
                        IP(dst=str(host))
                        / TCP(
                            sport=src_port, dport=dst_port, flags="S", seq=client_seq
                        ),
                        timeout=2,
                        verbose=0,
                    )
                    client_seq += 1

                    # print(ans.show())
                    if ans is None:
                        filteres_ports.append(port)
                        continue
                    elif ans.haslayer(TCP):
                        if ans[TCP].flags == "SA":  # this checks for SYN-ACK flags
                            server_seq = ans[TCP].seq
                            send(
                                IP(dst=str(host))
                                / TCP(
                                    sport=src_port,
                                    dport=dst_port,
                                    flags="R",
                                    seq=client_seq,
                                    ack=server_seq + 1,
                                ),
                                verbose=0,
                            )

                            open_ports.append(ans.sport)
                        elif (
                            ans[TCP].flags == "RA"  # This checks for RST-ACK flags
                        ):
                            closed_ports.append(ans.sport)
                print(open_ports)
                self.add_host(str(host), ports=open_ports)
                results.append(self.live_hosts[str(host)])
        except PermissionError as e:
            print(f"This must be run as Admin/root {e}")

        return results


if __name__ == "__main__":
    # test = networkMapper("192.168.1.0/24")
    # test = networkMapper("10.1.1.32/27")
    test = networkMapper("10.1.1.2")

    # results = test.arp_scan()
    # results = test.ping_network()
    # results = test.ping_network_fast()
    # print(results)
    # for host in test.live_hosts.values():
    #     print(host)
    results = test.tcp_syn(ports=[80, 443])
    # results = test.tcp_ack(ports=[80])
    # for host in test.live_hosts.values():
    #     print(host)
    print(test.live_hosts)
    print(results)
