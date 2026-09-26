import tkinter as tk
from tkinter import ttk
import networkmapper
import passwordcracker
import directorybuster
import wordpresslogin


class Header(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc | None = None,
    ) -> None:
        super().__init__(
            master,
        )
        ttk.Label(self, text="Hacking Tools", font=("Arial", 16)).pack(pady=10)


class Footer(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc | None = None,
    ) -> None:
        super().__init__(
            master,
        )
        ttk.Button(self, text="Exit").pack(side=tk.RIGHT, anchor="e", padx=10, pady=5)
        ttk.Button(self, text="Save & Exit").pack(
            side=tk.RIGHT, anchor="e", padx=10, pady=5
        )


class Sidebar(ttk.Frame):
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
        self.tree.item(mapper, open=True)

        cracking = self.tree.insert("", tk.END, text="Hash Cracker")
        # self.tree.insert(cracking, tk.END, text="Hash cracker")
        # self.tree.item(cracking, open=True)

        web = self.tree.insert("", tk.END, text="Web Hacking")
        self.tree.insert(web, tk.END, text="Directory Scanner")
        self.tree.insert(web, tk.END, text="Subdomain Scanner")
        self.tree.insert(web, tk.END, text="WordPress Login")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


#### Panels for the main part


class MainPanel(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc | None = None,
    ) -> None:
        super().__init__(
            master,
        )
        ttk.Label(self, text="Select a tool from the menu").pack(padx=20, pady=20)


class ArpPanel(ttk.Frame):
    def __init__(self, parent, networkmapper) -> None:
        super().__init__(parent)
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
        print("Add run logic here")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class IcmpPanel(ttk.Frame):
    def __init__(self, parent, networkmapper) -> None:
        super().__init__(parent)
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
        print("Hello world")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class TcpAckPanel(ttk.Frame):
    def __init__(self, parent, networkmapper) -> None:
        super().__init__(parent)
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
        print("Add Run logic here")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class TcpSynPanel(ttk.Frame):
    def __init__(self, parent, networkmapper) -> None:
        super().__init__(parent)
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
        print("Add logic")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class CrackerPanel(ttk.Frame):
    def __init__(self, parent, cracker) -> None:
        super().__init__(parent)
        self.cracker = cracker

        ttk.Label(self, text="Hash Cracker", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        ttk.Label(self, text="Single Hash (optional)").pack(anchor="w", padx=10)
        self.target_host_entry = ttk.Entry(self)
        self.target_host_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Hash File (optional)").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Hash Type (optional)").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Wordlist").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        print("Add logic")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class DirectoryBrutePanel(ttk.Frame):
    def __init__(self, parent, dirbuster) -> None:
        super().__init__(parent)
        self.dirbuster = dirbuster

        ttk.Label(self, text="Directory Scanner", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )

        ttk.Label(self, text="Target Host").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Wordlist").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(self, text="Run scanner", command=self.run).pack(
            anchor="w", padx=10, pady=5
        )

        self.output = tk.Text(self, height=10)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run(self):
        print("Add logic")

    def _log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)


class SubdirBrutePanel(ttk.Frame):
    def __init__(self, parent, dirbuster) -> None:
        super().__init__(parent)
        self.dirbuster = dirbuster

        ttk.Label(self, text="Subdirectory Scanner", font=("Arial", 13)).pack(
            anchor="w", padx=10, pady=(10, 5)
        )

        ttk.Label(self, text="Target Host").pack(anchor="w", padx=10)
        self.target_port_entry = ttk.Entry(self)
        self.target_port_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self, text="Wordlist").pack(anchor="w", padx=10)
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


class WpLoginPanel(ttk.Frame):
    def __init__(self, parent, wp_login) -> None:
        super().__init__(parent)
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
        self.footer = Footer(self)
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

        # Look up a panel for this name; parents ("Recon") won't be in the dict
        panel = self.main_panels.get(name, self.start_panel)
        panel.tkraise()


App()
