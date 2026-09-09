from ipaddress import IPv4Network
import random
from scapy.all import srp, Ether, ARP, ICMP, IP, sr, sr1, TCP, send


class networkMapper:
    def __init__(self, network: str, timeout: float = 2.0):
        self.network = IPv4Network(network)
        self.timeout = timeout

    # layer 2 scan
    def arp_scan(self) -> list[dict]:
        """Performs an ARP scan on local subnet to discover Host IPs and their MAC addresses

        This scan only works on local subnet (Layer 2) and is not able to traverse to another subnet.
        An intervall of 0.05 seconds have been chosen to allow for wifi connected devices to respond,
        and not falesly show up as non-responsive.

        returns:
            A list of dicts containing the IP addresses and MAC addresses of responsive and live hosts"""
        ans, _ = srp(
            Ether(dst="ff:ff:ff:ff:ff:ff")  # using all ff sends the packet to broadcast
            / ARP(pdst=str(self.network)),
            timeout=2,
            inter=0.05,  # Added intervall to allow for WiFi clients to respond.
        )
        results = [{"IP": r.psrc, "MAC": r.hwsrc} for _, r in ans]
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
        ans, _ = sr(
            IP(dst=str(network)) / ICMP(),
            timeout=2,
            verbose=0,
        )
        results = [{"IP": r.src} for _, r in ans]
        return results

    # this uses the sr1, firing one ping at the time, more stealthy
    # layer 3 scan
    def ping_network(self) -> tuple[list[dict], list[dict]]:
        """Performs an ICMP scan on selected network to fin live hosts

        This scan operates on Layer 3 and can be routed to selected network. By using the sr1 module
        this sends one ICMP packet at the time for a more stealthy approach.

        returns:
            A tuple with two lists, one with dicts of live hosts and one with dicts of blocked hosts.
        """
        addresses = self.network
        responding = []
        blocking = []
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
            elif int(ans.getlayer(ICMP).type) == 3 and int(
                ans.getlayer(ICMP).code
            ) in [  # type 3 is destination unreachable
                1,
                2,
                3,
                9,
                10,
                13,
            ]:
                blocking.append({"IP": str(host)})
            else:
                responding.append({"IP": str(host)})
        return responding, blocking

    # Layer 4 scan with TCP ACK
    def tcp_ack(self) -> list[dict]:
        """Performs a TCP ACK scan to reveal active hosts on selected network

        This scan sends an ACK packet to selected ports, if there is a service on the selected
        port, a RST packet is returned since we do not have a connection established. This method
        can penetrate stateless firewalls.

        returns:
            A list of dicts with the IP and open ports of live hosts."""
        addresses = self.network
        responding = []
        for host in addresses:
            if len(list(addresses)) > 1 and host in (
                addresses.network_address,
                addresses.broadcast_address,
            ):
                continue

            src_port = random.randint(1025, 65534)
            dst_port = 80
            ans = sr1(
                IP(dst=str(host)) / TCP(sport=src_port, dport=dst_port, flags="A"),
                timeout=2,
                verbose=0,
            )

            if ans is None:
                continue
            else:
                responding.append({"IP": str(host)})
        return responding

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
        result = []
        for host in addresses:
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

                if ans is None:
                    result.append(
                        {"IP": str(host), "PORT": dst_port, "State": "Filtered"}
                    )
                    continue
                elif ans.haslayer(TCP):
                    if ans[TCP].flags == "SA":  # this checks for SYN-ACK flags
                        server_seq = ans[TCP].seq
                        send_rst = send(
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
                        result.append(
                            {"IP": str(host), "PORT": dst_port, "State": "Open"}
                        )
                    elif (
                        ans[TCP].flags == "RA"  # This checks for RST-ACK flags
                    ):
                        result.append(
                            {"IP": str(host), "PORT": dst_port, "State": "Closed"}
                        )

        return result


if __name__ == "__main__":
    test = networkMapper("192.168.100.244")

    results = test.tcp_syn()
    # results = test.ping_network()
    # print(results)
