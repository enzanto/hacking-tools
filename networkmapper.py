from dataclasses import dataclass, field
from ipaddress import IPv4Network
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
    def __init__(self, network: str, timeout: float = 2.0):
        self.network = IPv4Network(network)
        self.timeout = timeout
        self.live_hosts = {}

    def add_host(
        self,
        ip: str,
        mac: str | None = None,
        ports: list[int] | None = None,
        live: bool = True,
    ):
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
    def arp_scan(self) -> list[dict]:
        """Performs an ARP scan on local subnet to discover Host IPs and their MAC addresses

        This scan only works on local subnet (Layer 2) and is not able to traverse to another subnet.
        An intervall of 0.05 seconds have been chosen to allow for wifi connected devices to respond,
        and not falesly show up as non-responsive.

        returns:
            A list of dicts containing the IP addresses and MAC addresses of responsive and live hosts"""
        results = []
        ans, _ = srp(
            Ether(dst="ff:ff:ff:ff:ff:ff")  # using all ff sends the packet to broadcast
            / ARP(pdst=str(self.network)),
            timeout=2,
            inter=0.05,  # Added intervall to allow for WiFi clients to respond.
        )
        for _, r in ans:
            self.add_host(r.psrc, mac=r.hwsrc)
            results.append(self.live_hosts[r.psrc])
        return results

    # This uses sr and nor sr1 - fires ALL pings at once = noisy noisy!
    # Layer 3 scan
    def ping_network_fast(
        self,
    ) -> list[dict]:
        """Performs an ICMP scan og selected network to find live hosts

        This scan operates on Layer 3 and can be routed to selected network. By using the sr module
        this sends all ICMP packets at once and is very noisy!

        returns:
            A list of dictionaries displaying the IP address of responsive hosts."""
        network = self.network
        results = []
        ans, _ = sr(
            IP(dst=str(network)) / ICMP(),
            timeout=2,
            verbose=0,
        )
        for _, r in ans:
            self.add_host(r.src)
            results.append(self.live_hosts[r.src])
        return results

    # this uses the sr1, firing one ping at the time, more stealthy
    # layer 3 scan
    def ping_network(self) -> list[dict]:
        """Performs an ICMP scan on selected network to fin live hosts

        This scan operates on Layer 3 and can be routed to selected network. By using the sr1 module
        this sends one ICMP packet at the time for a more stealthy approach.

        returns:
            A tuple with two lists, one with dicts of live hosts and one with dicts of blocked hosts.
        """
        addresses = self.network
        results = []
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
        return results

    # Layer 4 scan with TCP ACK
    def tcp_ack(self, ports: list[int] | None = None) -> list[dict]:
        """Performs a TCP ACK scan to reveal active hosts on selected network

        This scan sends an ACK packet to selected ports, if there is a service on the selected
        port, a RST packet is returned since we do not have a connection established. This method
        can penetrate stateless firewalls.

        returns:
            A list of dicts with the IP and open ports of live hosts."""  ## open ports can't be verified this way
        addresses = self.network
        if ports == None:
            ports = [80]  # Setting port 80 as standard, most likely to get thorugh FW
        results = []
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
                    IP(dst=str(host)) / TCP(sport=src_port, dport=dst_port, flags="A"),
                    timeout=2,
                    verbose=0,
                )
                # Maybe break after first validated response?
                if ans is None:
                    continue
                elif ans.haslayer(TCP) and ans[TCP].flags == "R":
                    self.add_host(ans.src)
                    results.append(self.live_hosts[ans.src])
        return results

    # Layer 4 scan with TCP syn
    def tcp_syn(self, ports: list[int] | None = None) -> list[dict]:
        """Performs a TCP SYN scan to reveal active hosts on selected network

        This scan sends an SYN packet to selected ports, if there is a service on the selected
        port, an ACK is recieved if the port is open. If an ACK is received and the port is open
        we close it gracefully with an RST packet. This method can penetrate stateful firewalls.

        returns:
            A list of dicts with the IP and open ports of live hosts."""
        addresses = self.network
        if ports == None:
            ports = [80]
        results = []
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
                    / TCP(sport=src_port, dport=dst_port, flags="S", seq=client_seq),
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
