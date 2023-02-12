#!/bin/bash
#Author: sidious

#Red color text output.
function ERROR(){
  echo >&2 "$(tput bold; tput setaf 1) ${*}$(tput sgr0)"
}

#Green color text output.
function MSG(){
  echo "$(tput bold; tput setaf 2) ${*}$(tput sgr0)"
}

#Root user check.
function ROOTPERM(){
  if [ "$(id -u)" -ne 0 ]; then ERROR "you must be root";exit 1;fi
}

#Output redirect to dev/null
function SILENT(){
    "$@" > /dev/null 2>&1
}

#Connectivity check.
function INET_CHECK(){
    IP="$(curl -s http://ifconfig.me)"
}

#Banner.
function BANNER(){
    printf "\n"
    cat << "EOF"

    ██╗  ██╗ █████╗ ██████╗ ██████╗ ███████╗███╗   ██╗
    ██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║
    ███████║███████║██████╔╝██║  ██║█████╗  ██╔██╗ ██║
    ██╔══██║██╔══██║██╔══██╗██║  ██║██╔══╝  ██║╚██╗██║
    ██║  ██║██║  ██║██║  ██║██████╔╝███████╗██║ ╚████║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝
                       -sidious-
EOF
printf "%20s $IP\n\n"
}

#Update and install upgrades.
function UPDATE_SYSTEM(){   
    printf "[*] Updating the system\n"
    SILENT apt update 
    SILENT apt upgrade --yes
    if [ $? -eq 0 ]; then printf "[*] Upgrading the system"; MSG "completed."; else printf "[!] Upgrades" ERROR "failed.";fi
    export PATH=$PATH:/usr/sbin
}

#Install fail2ban to protect against brute-force attacks.
function INSTALL_FAIL2BAN(){
    printf "[*] Installing fail2ban\n"
    SILENT apt install fail2ban --yes 
    if [ $? -eq 0 ]; then printf "[*] Installation";MSG "complete.";else printf "[!] Installation";ERROR "failed.";fi
}

#Harden ssh configuration.
function SSHD_CONFIG(){
    printf "[*] Configuring sshd config\n"
    mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
    cat <<EOT >/etc/ssh/sshd_config
Port 2107
Protocol 2
IgnoreRhosts yes
HostbasedAuthentication no
PermitRootLogin no
PermitEmptyPasswords no
X11Forwarding no
MaxAuthTries 5
ClientAliveInterval 900
ClientAliveCountMax 0
UsePAM yes
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
KexAlgorithms curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com
EOT
    SILENT systemctl restart sshd.service
    if [ $? -eq 0 ]; then printf "[*] Configuration of ssh";MSG "completed";else printf "[!] Configuration of ssh"; ERROR "failed";fi
}

#Setup firewall configuration.
function FIREWALL_CONFIG(){
    printf "[*] Configuring firewall\n"
    SILENT apt install ufw --yes 
    if [ $? -eq 0 ]; then printf "[*] Installation";MSG "complete";else printf "[*] Installation";ERROR "failed.";fi
    SILENT ufw default deny incoming 
    SILENT ufw default allow outgoing 
    SILENT ufw allow ssh 
    SILENT ufw allow 2107/tcp 
}

#Setup automatic updates.
function AUTO_UPDATES(){
    printf "[*] Configuring auto updates\n"
    SILENT apt install unattended-upgrades --yes
    if [ $? -eq 0 ]; then printf "[*] Configuration of auto updates"; MSG "completed";else printf "[!] Configuration of auto updates";ERROR "failed";fi
    cat << "EOF" >/etc/apt/apt.conf.d/20auto-upgrades
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
EOF
}

#Remove unnecessary packages and services.
function REMOVE_UNNECESARRY(){
    printf "[*] Removing unnecesarry packages\n"
    SILENT apt remove telnet* rsh-client* rsh-redone-client xinetd ypserv* tftp* openbsd-inetd bind9 --yes 
    if [ $? -eq 0 ]; then printf "[*] Removing packages";MSG "completed";else printf "[!] Removing packages";ERROR "failed";fi
}

#Enable auditd to track changes to the system.
function INSTALL_AUDITD(){
    printf "[*] Installing auditd\n"
    SILENT apt install auditd --yes
    if [ $? -eq 0 ]; then printf "[*] Installation";MSG "complete";else printf "[!] Installation";ERROR "failed.";fi
}

#Secure the GRUB bootloader.
function SECURE_GRUB(){
    printf "[*] Securing GRUB\n"
    sed -i s/GRUB_CMDLINE_LINUX=\"\"/GRUB_CMDLINE_LINUX=\"audit=1\"/ /etc/default/grub
    SILENT update-grub 
}

#Configure AppArmor to enforce security policies.
function INSTALL_APPARMOR(){
    printf "[*] Installing apparmor\n"
    SILENT apt install apparmor apparmor-utils --yes 
    if [ $? -eq 0 ]; then printf "[*] Installation";MSG "complete";else printf "[*] Installation";ERROR "failed.";fi
}

#Enable kernel protection features.
function CONFIGURE_KERNEL(){
    printf "[*] Configuring secure kernel settings\n"
    cat << "EOF" >>/etc/sysctl.conf
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
kernel.perf_event_paranoid = 2
kernel.randomize_va_space = 2
kernel.yama.ptrace_scope = 1
EOF
    SILENT sysctl -p
    if [ $? -eq 0 ]; then printf "[*] Configuration of kernel"; MSG "completed";else printf "[!] Configuration of kernel";ERROR "failed";fi
}


ROOTPERM
if [ $? -eq 0 ]; then INET_CHECK;BANNER;UPDATE_SYSTEM;INSTALL_FAIL2BAN;\
SSHD_CONFIG;FIREWALL_CONFIG;AUTO_UPDATES;REMOVE_UNNECESARRY;INSTALL_AUDITD;
SECURE_GRUB;INSTALL_APPARMOR;CONFIGURE_KERNEL; else
ERROR "You must be root"; exit 1;fi
