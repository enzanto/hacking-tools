from ipaddress import IPv4Network
from scapy.all import srp, Ether, ARP


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
        ans, unans = srp(
            Ether(dst="ff:ff:ff:ff:ff:ff")  # using all ff sends the packet to broadcast
            / ARP(pdst=str(self.network)),
            timeout=2,
            inter=0.05,  # Added intervall to allow for WiFi clients to respond.
        )
        results = [{"IP": r.psrc, "MAC": r.hwsrc} for _, r in ans]
        return results


test = networkMapper("192.168.1.0/24")

results = test.arp_scan()
print(results)
