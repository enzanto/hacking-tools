import tkinter as tk
from tkinter import ttk


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
        self.tree.insert(mapper, tk.END, text="ARP Scan")
        self.tree.insert(mapper, tk.END, text="ICMP Scan")
        self.tree.insert(mapper, tk.END, text="TCP-ACK scan")
        self.tree.insert(mapper, tk.END, text="TCP-SYN scan")
        self.tree.item(mapper, open=True)

        cracking = self.tree.insert("", tk.END, text="Hash cracker")
        # self.tree.insert(cracking, tk.END, text="Hash cracker")
        # self.tree.item(cracking, open=True)

        web = self.tree.insert("", tk.END, text="Web Hacking")
        self.tree.insert(web, tk.END, text="Directory Scan")
        self.tree.insert(web, tk.END, text="Subdomain Scan")
        self.tree.insert(web, tk.END, text="Wordpress Login")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


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
        self.header = Header(self)
        self.footer = Footer(self)
        self.menu = Sidebar(self)
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
        self.mainloop()


App()
