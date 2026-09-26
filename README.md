# Hacking Tools

This is a set of hacking tools built for my exam project at Noroff.

## Requirements

- Python3
- pip
- tkinter

### Windows
Windows also need to install npcap from [npcap.com](https://npcap.com/)


## Installation

First clone the repository

```bash
git clone https://github.com/enzanto/hacking-tools.git
```

```bash
python -m venv venv
```

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



