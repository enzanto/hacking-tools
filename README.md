# Hacking Tools

This is a set of hacking tools built for my exam project at Noroff.

## ⚠️ Legal Disclaimer

This project and its tools are provided for **educational purposes and authorized security testing only**.

The tools in this repository (network scanner, password cracker, directory/subdomain buster, and web login brute-forcer) are capable of actions that are **illegal without explicit, documented authorization** from the owner of the target system or network.

By using this software, you agree that:

- You will only use these tools against systems, networks, and accounts you **own** or have **explicit written permission** to test.
- The author assumes **no liability** for misuse, damage, or legal consequences resulting from the use of this software.
- This project is provided **"as is"**, without warranty of any kind.

Unauthorized access to computer systems is a criminal offence in most jurisdictions. If in doubt, don't run it against anything you don't have permission to test.


## Requirements

- Python3
- pip
- tkinter

### Windows
Windows also need to install npcap from [npcap.com](https://npcap.com/)


## Installation

### Nix

```bash
# GUI
nix run github:enzanto/hacking-tools
# CLI
nix run github:enzanto/hacking-tools#cli
```

### Windows and Linux

First clone the repository

```bash
git clone https://github.com/enzanto/hacking-tools.git
```

Create the virtual environment
```bash
python -m venv venv
```

Activate the virtual environment
windows

```powershell
# set execution policy first
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
# Activate the venv
./venv/Scripts/Activate.ps1
```

Linux
```bash
source venv/bin/activate
```


Install the required packages
```bash
pip install -r requirements.txt
```

for Linux, Tkinter must be installed via package manager, for windows it is packed with python

```bash
sudo apt install python3-tk      # Debian/Ubuntu
sudo dnf install python3-tkinter # Fedora
sudo pacman -S tk                # Arch
```


## Usage

From the virtual environment:

GUI mode
```bash
python main.py
```

CLI mode:
```bash
python main.py --cli
```



