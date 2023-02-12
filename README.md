# server-hardening

This is a linux hardening script for debian based servers.

## Usage:

```bash
██╗  ██╗ █████╗ ██████╗ ██████╗ ███████╗███╗   ██╗
██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║
███████║███████║██████╔╝██║  ██║█████╗  ██╔██╗ ██║
██╔══██║██╔══██║██╔══██╗██║  ██║██╔══╝  ██║╚██╗██║
██║  ██║██║  ██║██║  ██║██████╔╝███████╗██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝
                   -sidious-

# Git clone this repository:
$ git clone https://github.com/insidious-security/server-hardening.git

# Make the script exacutable:
$ chmod +x harden.sh

# Run the script as root:
$ sudo ./harden.sh
```
## Rather run it in python??
I have also added the same level of hardening written in python.

```bash
# Git clone this repository:
$ git clone https://github.com/insidious-security/server-hardening.git

# Install python dependency:
$ pip3 install requests 

# Run the code:
python3 harden.py
