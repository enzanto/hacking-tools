from dataclasses import asdict
from filehandler import write_json
import tkinter as tk
from tkinter import ttk, messagebox
from ipaddress import IPv4Network, AddressValueError, NetmaskValueError
import networkmapper
import passwordcracker
import directorybuster
import wordpresslogin


class Header(ttk.Frame):
    """This is the header panel of the gui

    args:
        master (tk.misc): the main frame calling this panel"""

    def __init__(
        self,
        master: tk.Misc | None = None,
    ) -> None:
        super().__init__(
            master,
        )
        ttk.Label(self, text="Hacking Tools", font=("Arial", 16)).pack(pady=10)


class Footer(ttk.Frame):
    """This is the footer panel of the gui

    contains buttons for save, and exit

    args:
        master (tk.misc): the main frame calling this panel"""

    def __init__(
        self,
        master: tk.Misc,
        net_scanner,
        password_cracker,
        directory_buster,
        wordpress_login,
    ) -> None:
        super().__init__(
            master,
        )
        self.net_scanner = net_scanner
        self.password_cracker = password_cracker
        self.directory_buster = directory_buster
        self.wordpress_login = wordpress_login
        ttk.Button(self, text="Exit", command=master.destroy).pack(
            side=tk.RIGHT, anchor="e", padx=10, pady=5
        )
        ttk.Button(self, text="Save & Exit", command=self.save).pack(
            side=tk.RIGHT, anchor="e", padx=10, pady=5
        )

    def save(self):
        loot_dict = {}
        loot_dict["hosts"] = {}
        loot_dict["passwords"] = []
        loot_dict["directories"] = {}
        loot_dict["logins"] = {}
        for host in self.net_scanner.live_hosts.items():
            loot_dict["hosts"][host[0]] = asdict(host[1])
        for pwd in self.password_cracker.cracked:
            loot_dict["passwords"].append(pwd)
        for dir in self.directory_buster.loot.items():
            loot_dict["directories"][dir[0]] = dir[1]
        for wp in self.wordpress_login.loot.items():
            loot_dict["logins"][wp[0]] = wp[1]

        filename = write_json(data=loot_dict)
        messagebox.showinfo("Loot saved", f"Loot saved to {filename}")
        self.master.destroy()


class Sidebar(ttk.Frame):
    """This is the sidebar panel of the gui

    This holds the treeview items of the menu.

    args:
        master (tk.misc): the main frame calling this panel"""

    def __init__(
        self,
        master: tk.Misc | None = None,
    ) -> None:
        super().__init__(
            master,
        )
        self.tree = ttk.Treeview(self)

        mapper = self.tree.insert("", tk.END, text="Network Mapper")
        self.tree.insert(mapper, tk.END, text="ARP Scanner")
        self.tree.insert(mapper, tk.END, text="ICMP Scanner")
        self.tree.insert(mapper, tk.END, text="TCP-ACK Scanner")
        self.tree.insert(mapper, tk.END, text="TCP-SYN Scanner")

        self.tree.insert("", tk.END, text="Hash Cracker")

        web = self.tree.insert("", tk.END, text="Web Hacking")
        self.tree.insert(web, tk.END, text="Directory Scanner")
        self.tree.insert(web, tk.END, text="Subdomain Scanner")
        self.tree.insert(web, tk.END, text="WordPress Login")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


#### Panels for the main part


class MainPanel(ttk.Frame):
    """This is the main panel of the gui

    This is the placeholder that displays when nothing is selected

    args:
        master (tk.misc): the main frame calling this panel"""

    def __init__(
        self,
        master: tk.Misc | None = None,
    ) -> None:
        super().__init__(
            master,
        )
        ttk.Label(self, text="Select a tool from the menu").pack(padx=20, pady=20)


class ArpPanel(ttk.Frame):
    """This is the ARP panel of the gui

    This arp panel, that has inputs for target host, a run button
    and a output panel

    args:
        master (tk.misc): the main frame calling this panel
        networkmapper: The network mapper function."""

    def __init__(self, master, networkmapper) -> None:
        super().__init__(master)
        self.networkmapper = networkmapper

        ttk.Label(self, text="ARP Scanner", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        ttk.Label(self, text="Target Host").pack(anchor="w", padx=10)
        self.target_host_entry = ttk.Entry(self)
        self.target_host_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        target_host = self.target_host_entry.get()
        if target_host == "":
            self._log("Please enter a network address")
            return
        try:
            validated_host = str(IPv4Network(target_host))
        except AddressValueError as e:
            self._log(f"Please select a valid address: {e}")
            return
        except NetmaskValueError as e:
            self._log(f"Please select a valid network mask: {e}")
            return
        except ValueError as e:
            self._log(f"unexpected value error: {e}")
            return
        except Exception as e:
            self._log(f"unexpected error: {e}")
            return

        self.networkmapper.arp_scan(network=validated_host)
        for host in self.networkmapper.live_hosts.values():
            self._log(f"IP: {host.ip} - MAC: {host.mac}")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class IcmpPanel(ttk.Frame):
    """This is the ICMP panel of the gui

    This ICMP panel, that has inputs for target host, a run button
    and a output panel

    args:
        master (tk.misc): the main frame calling this panel
        networkmapper: the networkmapper function"""

    def __init__(self, master, networkmapper) -> None:
        super().__init__(master)
        self.networkmapper = networkmapper

        ttk.Label(self, text="ICMP Scanner", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        ttk.Label(self, text="Target Host").pack(anchor="w", padx=10)
        self.target_host_entry = ttk.Entry(self)
        self.target_host_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        target_host = self.target_host_entry.get()
        if target_host == "":
            self._log("Please enter a network address")
            return
        try:
            validated_host = str(IPv4Network(target_host))
        except AddressValueError as e:
            self._log(f"Please select a valid address: {e}")
            return
        except NetmaskValueError as e:
            self._log(f"Please select a valid network mask: {e}")
            return
        except ValueError as e:
            self._log(f"unexpected value error: {e}")
            return
        except Exception as e:
            self._log(f"unexpected error: {e}")
            return

        self.networkmapper.ping_network(network=validated_host)
        for host in self.networkmapper.live_hosts.values():
            self._log(f"IP: {host.ip}")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class TcpAckPanel(ttk.Frame):
    """This is the TCP-ACK panel of the gui

    This TCP-ACK panel, that has inputs for target host, a run button
    and a output panel

    args:
        master (tk.misc): the main frame calling this panel
        networkmapper: the networkmapper function"""

    def __init__(self, master, networkmapper) -> None:
        super().__init__(master)
        self.networkmapper = networkmapper

        ttk.Label(self, text="TCP-ACK Scanner", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        ttk.Label(self, text="Target Host").pack(anchor="w", padx=10)
        self.target_host_entry = ttk.Entry(self)
        self.target_host_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        target_host = self.target_host_entry.get()
        if target_host == "":
            self._log("Please enter a network address")
            return
        try:
            validated_host = str(IPv4Network(target_host))
        except AddressValueError as e:
            self._log(f"Please select a valid address: {e}")
            return
        except NetmaskValueError as e:
            self._log(f"Please select a valid network mask: {e}")
            return
        except ValueError as e:
            self._log(f"unexpected value error: {e}")
            return
        except Exception as e:
            self._log(f"unexpected error: {e}")
            return

        print(validated_host)
        print(str(validated_host))
        self.networkmapper.tcp_ack(network=validated_host)
        for host in self.networkmapper.live_hosts.values():
            self._log(f"IP: {host.ip}")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class TcpSynPanel(ttk.Frame):
    """This is the TCP-SYN panel of the gui

    This TCP-SYN panel, that has inputs for target host, target ports,
    a run button and an output panel

    args:
        master (tk.misc): the main frame calling this panel
        networkmapper: the networkmapper function"""

    def __init__(self, master, networkmapper) -> None:
        super().__init__(master)
        self.networkmapper = networkmapper

        ttk.Label(self, text="TCP-SYN Scanner", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        ttk.Label(self, text="Target Host").pack(anchor="w", padx=10)
        self.target_host_entry = ttk.Entry(self)
        self.target_host_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Target Port").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        target_host = self.target_host_entry.get()
        if target_host == "":
            self._log("Please enter a network address")
            return
        try:
            validated_host = str(IPv4Network(target_host))
        except AddressValueError as e:
            self._log(f"Please select a valid address: {e}")
            return
        except NetmaskValueError as e:
            self._log(f"Please select a valid network mask: {e}")
            return
        except ValueError as e:
            self._log(f"unexpected value error: {e}")
            return
        except Exception as e:
            self._log(f"unexpected error: {e}")
            return

        ports = self.target_port_entry.get()
        self.networkmapper.tcp_syn(network=validated_host, ports=ports)
        for host in self.networkmapper.live_hosts.values():
            self._log(f"IP: {host.ip} - Ports: {host.ports}")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class CrackerPanel(ttk.Frame):
    """This is the password cracker panel of the gui

    This password cracker panel, that has inputs for hash file, wordlist,
    and a output panel

    args:
        master (tk.misc): the main frame calling this panel
        cracker: The password cracker module
    """

    def __init__(self, master, cracker) -> None:
        super().__init__(master)
        self.cracker = cracker

        ttk.Label(self, text="Hash Cracker", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        ttk.Label(self, text="Hash File").pack(anchor="w", padx=10)
        self.hash_file = ttk.Entry(self)
        self.hash_file.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Wordlist").pack(anchor="w", padx=10)
        self.wordlist = ttk.Entry(self)
        self.wordlist.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        hash_file = self.hash_file.get() if self.hash_file.get() != "" else None
        wordlist = self.wordlist.get() if self.wordlist.get() != "" else None
        self.cracker.hash_cracker(wordlist=wordlist, hashlist=hash_file)
        for pwd in self.cracker.cracked.values():
            self._log(
                f"password: {pwd['password']}, Hash type: {pwd['type']}, Hash: {pwd['hash']}"
            )

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class DirectoryBrutePanel(ttk.Frame):
    """This is the directory brute panel of the gui

    This directory brute panel, that has inputs for target host, wordlist
    and a output panel

    args:
        master (tk.misc): the main frame calling this panel
        dirbuster: The directory buster
    """

    def __init__(self, master, dirbuster) -> None:
        super().__init__(master)
        self.dirbuster = dirbuster

        ttk.Label(self, text="Directory Scanner", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )

        ttk.Label(self, text="Target Host").pack(anchor="w", padx=10)
        self.target_host_entry = ttk.Entry(self)
        self.target_host_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Wordlist").pack(anchor="w", padx=10)
        self.wordlist_entry = ttk.Entry(self)
        self.wordlist_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        target_host = self.target_host_entry.get()
        wordlist = self.wordlist_entry.get()
        self.dirbuster.directory_brute(target=target_host, wordlist=wordlist)
        for dir in self.dirbuster.loot.items():
            for dirs in dir[1]:
                self._log(dirs)

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class SubdirBrutePanel(ttk.Frame):
    """This is the subdomain brute panel of the gui

    This subdomain brute panel, that has inputs for target host, wordlist
    and a output panel

    args:
        master (tk.misc): the main frame calling this panel
        dirbuster: The directory buster
    """

    def __init__(self, master, dirbuster) -> None:
        super().__init__(master)
        self.dirbuster = dirbuster

        ttk.Label(self, text="Subdirectory Scanner", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )

        ttk.Label(self, text="Target Host").pack(anchor="w", padx=10)
        self.target_host_entry = ttk.Entry(self)
        self.target_host_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Wordlist").pack(anchor="w", padx=10)
        self.wordlist_entry = ttk.Entry(self)
        self.wordlist_entry.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        target_host = self.target_host_entry.get()
        wordlist = self.wordlist_entry.get()
        self.dirbuster.subdomain_brute(target=target_host, wordlist=wordlist)
        for dir in self.dirbuster.loot.items():
            for dirs in dir[1]:
                self._log(dirs)

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class WpLoginPanel(ttk.Frame):
    """This is the WordPress login panel of the gui

    This  WordPress login panel, that has inputs for target host, userlist,
    passlist and a output panel

    args:
        master (tk.misc): the main frame calling this panel
        wp_login: the wordpress login function.
    """

    def __init__(self, master, wp_login) -> None:
        super().__init__(master)
        self.wp_login = wp_login

        ttk.Label(self, text="WordPress Login", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )

        ttk.Label(self, text="Target Host").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="User (optional)").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Userlist (optional)").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Password (optional)").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Password list (optional)").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        print("Logic")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class App(tk.Tk):
    """The main App program for the GUI

    This class initializes all the scanners and tools, sets the layout
    then packs the panels in to the correct locations."""

    def __init__(
        self,
        screenName: str | None = None,
        baseName: str | None = None,
        className: str = "Tk",
        useTk: bool = True,
        sync: bool = False,
        use: str | None = None,
    ) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title("Hacking tools")
        # initialize imported tools
        self.networkmapper = networkmapper.NetworkMapper()
        self.cracker = passwordcracker.PasswordCracker()
        self.dirbuster = directorybuster.DirectoryBuster()
        self.wp_login = wordpresslogin.WordpressLogin()
        # create panels
        self.header = Header(self)
        self.footer = Footer(
            self,
            net_scanner=self.networkmapper,
            password_cracker=self.cracker,
            directory_buster=self.dirbuster,
            wordpress_login=self.wp_login,
        )
        self.menu = Sidebar(self)
        # Main panels in a selectable dict
        self.main_panels = {
            "ARP Scanner": ArpPanel(self, self.networkmapper),
            "ICMP Scanner": IcmpPanel(self, self.networkmapper),
            "TCP-ACK Scanner": TcpAckPanel(self, self.networkmapper),
            "TCP-SYN Scanner": TcpSynPanel(self, self.networkmapper),
            "Hash Cracker": CrackerPanel(self, self.cracker),
            "Directory Scanner": DirectoryBrutePanel(self, self.dirbuster),
            "Subdomain Scanner": SubdirBrutePanel(self, self.dirbuster),
            "WordPress Login": WpLoginPanel(self, self.wp_login),
        }
        self.start_panel = MainPanel(self)
        # GUI layout
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        # Place elements in the grid
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.menu.grid(row=1, column=0, sticky="nsew")
        self.footer.grid(row=2, column=0, columnspan=2, sticky="nsew")
        for panel in self.main_panels.values():
            panel.grid(row=1, column=1, sticky="nsew")
        self.start_panel.grid(row=1, column=1, sticky="nsew")
        self.menu.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.mainloop()

    def on_select(self, event):
        selection = self.menu.tree.selection()
        if not selection:
            return
        name = self.menu.tree.item(selection[0], "text")

        panel = self.main_panels.get(name, self.start_panel)
        panel.tkraise()


if __name__ == "__main__":
    App()
