<div align="center">

# 📡 RS WiFi Cracker PRO v4

**The ultimate WiFi security testing toolkit — 50+ attack modules, GPU acceleration, AI-powered features, and enterprise-grade reliability**

[![Language](https://img.shields.io/badge/Language-Python-yellow?logo=python)](https://python.org)
[![Version](https://img.shields.io/badge/Version-4.0%20Ultimate-red)](https://github.com/rajsaraswati-jatavv/RS-WiFi-Cracker-PRO-v4/releases)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-blue?logo=linux)](https://www.kali.org)
[![YouTube](https://img.shields.io/badge/YouTube-T3rmuxk1ng-red?logo=youtube)](https://youtube.com/@T3rmuxk1ng)
[![License](https://img.shields.io/badge/License-Educational-yellow)](./LICENSE)

*Built with 💚 by [T3rmuxk1ng](https://youtube.com/@T3rmuxk1ng)*

</div>

---

## 🎬 Demo & Tutorials

📺 **Watch on YouTube**: [https://youtube.com/@T3rmuxk1ng](https://youtube.com/@T3rmuxk1ng)

Subscribe for WiFi hacking tutorials, advanced pentesting demos, and exclusive tool releases!

---

## ✨ Features

### 🎯 Core Attack Modules

| Module | Description |
|--------|-------------|
| **Advanced Network Scanner** | Multi-backend scanning (airodump-ng, scapy, nmcli) |
| **WPA/WPA2 Handshake Capture** | Multiple capture modes with auto-deauth |
| **GPU-Accelerated Cracking** | Hashcat integration for fast cracking |
| **AI-Powered Password Generation** | Smart wordlist creation |
| **Real-Time Monitoring** | Live scan updates and statistics |
| **WPS Attack Suite** | Pixie Dust, PIN Brute Force, Null PIN |
| **PMKID Attack** | Offline attack without connected clients |
| **Evil Twin** | Rogue AP with captive portal |
| **Deauth Attack** | Multiple modes (broadcast, targeted, persistent) |
| **Karma Attack** | Auto-connect exploitation |
| **MITM Suite** | ARP spoof, DNS spoof, SSL strip |

### 🚀 Enterprise Features

- **Web Dashboard** — Browser-based control panel
- **RESTful API** — Automation-ready API server
- **Plugin Architecture** — Extensible module system
- **Comprehensive Logging** — Detailed audit trails
- **Database Storage** — SQLite for results and statistics
- **Configuration System** — JSON-based config management

---

## 🛠️ Requirements

| Requirement | Details |
|-------------|---------|
| OS | Kali Linux 2024.x (recommended) |
| Python | 3.11+ |
| WiFi Adapter | Must support monitor mode & packet injection |
| Privileges | Root (sudo) required |

### System Dependencies
```bash
# Aircrack-ng suite, reaver, bully, hashcat, john, hydra
# hcxdumptool, hcxtools
```

### Python Packages
```bash
pip3 install scapy requests colorama rich psutil
```

---

## 🚀 Installation

### Quick Install
```bash
git clone https://github.com/rajsaraswati-jatavv/RS-WiFi-Cracker-PRO-v4.git
cd RS-WiFi-Cracker-PRO-v4
chmod +x install.sh
sudo ./install.sh
```

### Run
```bash
# Interactive mode
sudo python3 rs_wifi_pro.py

# CLI mode
sudo python3 rs_wifi_pro.py -i wlan0 --scan
sudo python3 rs_wifi_pro.py -i wlan0 --attack wps --target AA:BB:CC:DD:EE:FF
sudo python3 rs_wifi_pro.py --crack capture.cap -w wordlist.txt
```

---

## 📖 Usage

### Attack Methods

| Attack | Speed | Requirements |
|--------|-------|-------------|
| **WPS Pixie Dust** | 1-60 seconds | Vulnerable router |
| **PMKID Attack** | Minutes | hcxdumptool, no client needed |
| **Handshake Capture** | Variable | Active client on network |
| **Evil Twin** | Variable | Social engineering setup |

### Configuration

Edit `config/config.json`:
```json
{
  "general": {
    "interface": "wlan0",
    "log_level": "INFO"
  },
  "scanning": {
    "default_duration": 30
  },
  "cracking": {
    "default_wordlist": "/usr/share/wordlists/rockyou.txt",
    "use_gpu": true
  }
}
```

---

## 📁 Project Structure

```
RS-WiFi-Cracker-PRO-v4/
├── rs_wifi_pro.py          # Main entry point
├── install.sh              # Installation script
├── core/                   # Core modules
│   ├── scanner.py          # Network scanner
│   ├── capturer.py         # Handshake capture
│   ├── cracker.py          # Password cracker
│   ├── attacker.py         # Attack engine
│   └── types.py            # Type definitions
├── modules/                # Attack modules
│   ├── wps_attack.py       # WPS attacks
│   ├── evil_twin.py        # Evil Twin
│   ├── pmkid.py            # PMKID attack
│   ├── deauth.py           # Deauth attack
│   ├── karma.py            # Karma attack
│   └── mitm.py             # MITM suite
├── utils/                  # Utilities
│   ├── logger.py           # Logging system
│   ├── config.py           # Configuration
│   ├── interface.py        # Interface manager
│   └── wordlist.py         # Wordlist generator
├── plugins/                # Plugin system
├── api/                    # REST API
├── web/                    # Web dashboard
├── config/                 # Configuration files
├── data/                   # Database storage
├── captures/               # Captured handshakes
├── reports/                # Generated reports
└── wordlists/              # Password wordlists
```

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](./.github/README.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

**This tool is for AUTHORIZED SECURITY TESTING and EDUCATIONAL purposes only.**

- Only use on networks you own or have explicit written permission to test
- Unauthorized access to computer networks is illegal in most jurisdictions
- The developers are not liable for any misuse or damage caused
- Always comply with local laws and regulations

---

## 📺 YouTube

📺 **T3rmuxk1ng** — [https://youtube.com/@T3rmuxk1ng](https://youtube.com/@T3rmuxk1ng)

Subscribe for:
- Advanced WiFi hacking tutorials & demos
- Network security walkthroughs
- Cybersecurity tips & tricks
- Exclusive tool releases

---

<div align="center">

**Built with 💚 by [T3rmuxk1ng](https://youtube.com/@T3rmuxk1ng)**

⭐ If you like this project, give it a star!

</div>
