# Author:sidious
import os
import requests
import subprocess as subp


# Define color support
CYA = '\033[96m'
GRE = '\033[92m'
RED = '\033[31m'
NOR = '\033[0m'


#Check network connectivity
def inet_check():
    try:
        global ip
        ip = requests.get("http://ifconfig.me")
        if ip.status_code == 200:
            ip = ip.text.strip()
        else:
            print(F"[!]Internet connectivity{RED}failed{NOR}.")
            exit()
    except (ConnectionResetError, ConnectionRefusedError) as error:
        print("[!]Connecting to ifconfig.me failed. Test your internet connection manually.")
        exit()

#Banner inlcuding IPaddress
def banner():
    print(f'''\n{CYA}
██╗  ██╗ █████╗ ██████╗ ██████╗ ███████╗███╗   ██╗
██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║
███████║███████║██████╔╝██║  ██║█████╗  ██╔██╗ ██║
██╔══██║██╔══██║██╔══██╗██║  ██║██╔══╝  ██║╚██╗██║
██║  ██║██║  ██║██║  ██║██████╔╝███████╗██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝
            -sidious-
        IP:{NOR} {ip}                                           
''')

# Update the system
def update_config():
    print(f"[{CYA}*{NOR}]Attempting {CYA}OS updates{NOR}, please hold")
    update = subp.run(["apt", "update"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    upgrade = subp.run(["apt", "upgrade", "-y"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    cmd = "export PATH=$PATH:/usr/sbin"
    os.system(cmd)
    if upgrade.returncode == 0:
        print(f"[{GRE}*{NOR}]OS updates {GRE}completed.{NOR}")
    else:
        print(f"[!]OS update {RED}failed.{NOR}")
        exit()

# Install fail2ban to protect against brute-force attacks
def fail2ban_config():
    print(f"[{CYA}*{NOR}]Attempting to install{CYA} fail2ban{NOR}")
    fail2ban = subp.run(["apt", "install", "fail2ban", "-y"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    if fail2ban.returncode == 0:
        print(f"[{GRE}*{NOR}]Installation of fail2ban {GRE}completed{NOR}.")
    else:
        print(f"[{RED}!{NOR}]Installation of fail2ban {RED}failed{NOR}.")
        exit()

# Set the SSH port to a non-standard port
def sshd_hardening():
    print(f"[{CYA}*{NOR}]Attempting to configure {CYA}sshd_config{NOR}")
    subp.run(["mv", "/etc/ssh/sshd_config", "/etc/ssh/sshd_config.bak"])
    file = open("sshd_config", "w")
    file.write('''Protocol 2\nIgnoreRhosts yes\nHostbasedAuthentication no\nPermitRootLogin no\nPermitEmptyPasswords no\nX11Forwarding no\nMaxAuthTries 5\nClientAliveInterval 900\nClientAliveCountMax 0\nUsePAM yes\nHostKey /etc/ssh/ssh_host_ed25519_key\nHostKey /etc/ssh/ssh_host_rsa_key\nKexAlgorithms curve25519-sha256@libssh.org\nCiphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr\nMACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com\n''')
    subp.run(["mv", "sshd_config", "/etc/ssh/"])
    restart_sshd = subp.run(["systemctl", "restart", "sshd.service"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    if restart_sshd.returncode == 0:
        print(f"[{GRE}*{NOR}]sshd configuration {GRE}completed{NOR}")
    else:
        print(f"[{RED}!{NOR}]sshd configuration {RED}failed{NOR}")

# Set up a firewall
def firewall_config():
    print(f"[{CYA}*{NOR}]Attempting to install {CYA}ufw firewall rules{NOR}")
    install_uwf = subp.run(["apt", "install", "ufw", "-y"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    subp.run(["ufw", "default", "deny", "incoming"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    subp.run(["ufw", "default", "allow", "outgoing"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    subp.run(["ufw", "allow", "ssh"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    subp.run(["ufw", "allow", "2107/tcp"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    enable_rules = subp.run(["ufw", "enable"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    if install_uwf.returncode == 0:
        print(f"[{GRE}*{NOR}]Installation of ufw {GRE}completed{NOR}.")  
    else:
        print(f"[!]Installation of ufw {GRE}failed{NOR}.")
    if enable_rules.returncode == 0:
        print(f"[{GRE}*{NOR}]Configuration of firewall rules is {GRE}completed{NOR}")
    else:
        print(f"[{RED}!{NOR}]Configuration of firewall rules {RED}failed{NOR}.")

def auto_updates():
    auto_up = input(f"[{CYA}*{NOR}]Would you like to have auto updates enabled press y/n: ")
    if auto_up == "y":
        print(f"[{CYA}*{NOR}]Attempting to configure {CYA}unattended-upgrades{NOR}")
        subp.run(["apt", "install", "unattended-upgrades", "-y"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
        with open("/etc/apt/apt.conf.d/20auto-upgrades", "a") as f:
            f.write('APT::Periodic::Update-Package-Lists "1";\n')
            f.write('APT::Periodic::Unattended-Upgrade "1";\n')
    elif auto_up == "n":
        print(f"[{GRE}*{NOR}]Skipping{CYA} unattended-upgrades{NOR}")
        pass
    else:
        print(f"[{RED}!{NOR}]Did not select an option, skipping")
        pass

# Remove unnecessary packages and services
def remove_unn():
    print(f"[{CYA}*{NOR}]Attempting to remove {CYA}unnecesarry packages{NOR}")
    unnecessary_packages = subp.run(["apt", "remove", "telnet*", "rsh-client*", "rsh-redone-client", "talk*",
     "xinetd", "ypserv*", "tftp*", "openbsd-inetd", "bind9", "-y"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    if unnecessary_packages.returncode == 0:
        print(f"[{GRE}*{NOR}]Removing unnecessary packages {GRE}completed{NOR}.")
    else:
        print(f"[{RED}!{NOR}]Removing of unnecessary packages {RED}failed{NOR}.")

# Enable auditd to track changes to the system
def install_auditd():
    print(f"[{CYA}*{NOR}]Attempting to install {CYA}auditd{NOR}")
    auditd = subp.run(["apt", "install", "auditd", "-y"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    if auditd.returncode == 0:
        print(f"[{GRE}*{NOR}]Installation of auditd {GRE}completed{NOR}.")
    else:
        print(f"[{RED}!{NOR}]Installation of auditd {RED}failed{NOR}.")

# Secure the GRUB bootloader
def secure_grub():
    print(f"[{CYA}*{NOR}]Attempting to {CYA}secure GRUB{NOR}")
    subp.run(["sed", "-i", "s/GRUB_CMDLINE_LINUX=\"\"/GRUB_CMDLINE_LINUX=\"audit=1\"/", "/etc/default/grub"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    update_grub = subp.run(["update-grub"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    if update_grub.returncode == 0:
        print(f"[{GRE}*{NOR}]Secure configuartion of grub {GRE}completed{NOR}.")
    else:
        print(f"[{RED}!{NOR}]Secure configuration of grub {RED}failed{NOR}.")

# Configure AppArmor to enforce security policies
def install_apparmor():
    apparmor_config = input(f"[{CYA}*{NOR}]Would you like to install AppArmor on the system? Press y/n: ")
    if apparmor_config == "y":
        print(f"[{CYA}*{NOR}]Attempting to install {CYA}AppArmor{NOR}")
        install_apparmor = subp.run(["apt", "install", "apparmor", "apparmor-utils", "-y"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
        if install_apparmor.returncode == 0:
            print(f"[{GRE}*{NOR}]Installation of AppArmor is {GRE}completed{NOR}")
        else:
            print(f"[{RED}!{NOR}]Installation of AppArmor {GRE}failed{NOR}.")
    elif apparmor_config == "n":
        print(f"[{GRE}*{NOR}]Skipping installation of {CYA}AppArmor{NOR}")
    else:
        print("Did not select an option, skipping")
        pass

# Enable kernel protection features
def kernel_hardening():
    print(f"[{CYA}*{NOR}]Attempting to hardenen the {CYA}kernel{NOR}")
    with open("/etc/sysctl.conf", "a") as f:
        f.write('kernel.kptr_restrict = 2\n')
        f.write('kernel.dmesg_restrict = 1\n')
        f.write('kernel.perf_event_paranoid = 2\n')
        f.write('kernel.randomize_va_space = 2\n')
        f.write('kernel.yama.ptrace_scope = 1\n')
        f.write('kernel.yama.protected_nonaccess_hardlinks = 1\n')
        f.write('kernel.yama.protected_sticky_symlinks = 1\n') 
    reload_mod = subp.run(["sysctl", "-p"], stdout=subp.DEVNULL, stderr=subp.DEVNULL)
    if reload_mod.returncode == 255:
        print(f"[{GRE}*{NOR}]Kernel hardening {GRE}completed{NOR}")
    else:
        print(f"[{RED}!{NOR}]Kernel hardening {RED}failed{NOR}.")

if __name__ == '__main__':
    try:
        inet_check()
        banner()
        update_config()
        fail2ban_config()
        sshd_hardening()
        firewall_config()
        auto_updates()
        remove_unn()
        install_auditd()
        secure_grub()
        install_apparmor()
        kernel_hardening()
    except KeyboardInterrupt:
        print("\nExited by user.")
        exit()
    except Exception as error:
        print(error)
        exit()
