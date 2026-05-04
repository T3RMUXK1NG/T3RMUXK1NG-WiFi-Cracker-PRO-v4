#!/bin/bash
#
#  T3RMUXK1NG WiFi Cracker PRO v4.0 - Installation Script
#  T3rmuxk1ng Private Release
#  Production Ready - Ultimate Edition
#

set -e

R='\033[91m'
G='\033[92m'
Y='\033[93m'
C='\033[96m'
W='\033[97m'
RESET='\033[0m'

echo -e "${C}"
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║          T3RMUXK1NG WiFi Cracker PRO v4.0 - Ultimate Edition              ║"
echo "║                    T3rmuxk1ng Private Release                      ║"
echo "║                      Production Ready Build                        ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Check root
if [ "$EUID" -ne 0 ]; then
    echo -e "${Y}[!] Run with sudo: sudo bash install.sh${RESET}"
    exit 1
fi

# Detect OS
if [ -f /etc/kali-release ]; then
    OS="kali"
elif [ -f /etc/debian_version ]; then
    OS="debian"
elif [ -f /etc/arch-release ]; then
    OS="arch"
else
    OS="unknown"
fi

echo -e "${C}[*] Detected OS: $OS${RESET}"

# Update system
echo -e "${C}[*] Updating system...${RESET}"
apt-get update -y 2>/dev/null || true

# Install dependencies
echo -e "${C}[*] Installing dependencies...${RESET}"

PACKAGES=(
    # Python
    python3 python3-pip python3-dev python3-venv
    
    # WiFi tools
    aircrack-ng reaver bully hashcat john hydra
    macchanger wireless-tools iw net-tools
    
    # Network tools
    hostapd dnsmasq nmap tshark wireshark
    bettercap hcxdumptool hcxtools
    
    # System tools
    git wget curl tmux htop
    pciutils usbutils
)

for pkg in "${PACKAGES[@]}"; do
    echo -e "${Y}[*] Installing $pkg...${RESET}"
    apt-get install -y $pkg 2>/dev/null || echo -e "${Y}[!] $pkg installation skipped${RESET}"
done

# Python packages
echo -e "${C}[*] Installing Python packages...${RESET}"
pip3 install --upgrade pip 2>/dev/null || true
pip3 install scapy requests colorama tqdm rich tabulate psutil netifaces 2>/dev/null || true

# Create directories
echo -e "${C}[*] Creating directories...${RESET}"
mkdir -p /opt/t3rmuxk1ng-wifi-pro-v4
mkdir -p /usr/share/wordlists/rs-wordlists
mkdir -p /var/log/t3rmuxk1ng-wifi-pro
mkdir -p ~/.config/t3rmuxk1ng-wifi-pro

# Copy files
echo -e "${C}[*] Installing T3RMUXK1NG WiFi Cracker PRO...${RESET}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -r "$SCRIPT_DIR"/* /opt/t3rmuxk1ng-wifi-pro-v4/
chmod +x /opt/t3rmuxk1ng-wifi-pro-v4/t3rmuxk1ng_wifi_pro.py

# Create symlink
ln -sf /opt/t3rmuxk1ng-wifi-pro-v4/t3rmuxk1ng_wifi_pro.py /usr/local/bin/t3rmuxk1ng-wifi-pro 2>/dev/null || true

# Generate wordlists
echo -e "${C}[*] Generating wordlists...${RESET}"
python3 -c "
from utils.wordlist import WordlistGenerator
gen = WordlistGenerator()
gen.common('/usr/share/wordlists/rs-wordlists/common.txt', 500000)
print('Wordlist generated')
" 2>/dev/null || echo -e "${Y}[!] Wordlist generation skipped${RESET}"

# Create bash alias
echo "alias rs-wifi='sudo python3 /opt/t3rmuxk1ng-wifi-pro-v4/t3rmuxk1ng_wifi_pro.py'" >> /etc/bash.bashrc 2>/dev/null || true

# Create desktop entry
cat > /usr/share/applications/t3rmuxk1ng-wifi-pro.desktop << EOF
[Desktop Entry]
Name=T3RMUXK1NG WiFi Cracker PRO
Comment=T3RMUXK1NG WiFi Cracker PRO v4.0 - Ultimate Edition
Exec=sudo python3 /opt/t3rmuxk1ng-wifi-pro-v4/t3rmuxk1ng_wifi_pro.py
Icon=network-wireless
Terminal=true
Type=Application
Categories=Network;Security;
EOF

echo -e "${G}"
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║              INSTALLATION COMPLETE!                               ║"
echo "║                                                                   ║"
echo "║  T3RMUXK1NG WiFi Cracker PRO v4.0 - Ultimate Edition                     ║"
echo "║  T3rmuxk1ng Private Release                                       ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

echo ""
echo -e "${G}Usage:${RESET}"
echo -e "  ${W}t3rmuxk1ng-wifi-pro${RESET}              # Interactive mode"
echo -e "  ${W}sudo python3 /opt/t3rmuxk1ng-wifi-pro-v4/t3rmuxk1ng_wifi_pro.py${RESET}"
echo ""
echo -e "${G}Features:${RESET}"
echo -e "  ${W}• Network Scanner (airodump, scapy, nmcli)${RESET}"
echo -e "  ${W}• WPA/WPA2 Handshake Capture${RESET}"
echo -e "  ${W}• WPS Attack Suite (Pixie Dust, Brute Force)${RESET}"
echo -e "  ${W}• PMKID Attack${RESET}"
echo -e "  ${W}• Evil Twin with Captive Portal${RESET}"
echo -e "  ${W}• Deauthentication Attack${RESET}"
echo -e "  ${W}• Karma Attack${RESET}"
echo -e "  ${W}• MITM Attack Suite${RESET}"
echo -e "  ${W}• GPU-Accelerated Cracking${RESET}"
echo -e "  ${W}• AI-Powered Password Generation${RESET}"
echo ""
echo -e "${G}Wordlists:${RESET}"
echo -e "  ${W}/usr/share/wordlists/rs-wordlists/common.txt${RESET}"
echo ""
echo -e "${Y}For authorized security testing only!${RESET}"
