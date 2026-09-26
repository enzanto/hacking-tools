import tkinter as tk
from tkinter import ttk
import networkmapper


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
        # create panels
        self.header = Header(self)
        self.footer = Footer(self)
        self.menu = Sidebar(self)
        # Main panels in a selectable dict
        self.main_panels = {"ARP Scan": ArpPanel(self, self.networkmapper)}
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
