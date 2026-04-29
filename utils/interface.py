#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - Interface Manager Utility"""

import os
import re
import subprocess
import random
from typing import Dict, List, Optional
from pathlib import Path

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
W = '\033[97m'
RESET = '\033[0m'


class InterfaceManager:
    """WiFi Interface Management"""
    
    OUI_DB: Dict[str, str] = {}
    
    def __init__(self):
        self.interfaces: List[Dict] = []
        self.selected: Optional[str] = None
        self.monitor_interface: Optional[str] = None
        self._load_oui()
    
    def _load_oui(self):
        if self.OUI_DB:
            return
        for path in ['/usr/share/ieee-data/oui.txt', '/usr/share/wireshark/manuf']:
            if os.path.exists(path):
                try:
                    with open(path, 'r', errors='ignore') as f:
                        for line in f:
                            if ':' in line:
                                parts = line.strip().split()
                                if parts:
                                    prefix = parts[0].replace(':', '').upper()[:6]
                                    vendor = parts[-1] if len(parts) > 1 else 'Unknown'
                                    self.OUI_DB[prefix] = vendor
                except:
                    pass
                break
    
    def get_vendor(self, mac: str) -> str:
        prefix = mac.replace(':', '').upper()[:6]
        return self.OUI_DB.get(prefix, 'Unknown')
    
    def list_interfaces(self) -> List[Dict]:
        self.interfaces = []
        net_dir = '/sys/class/net'
        
        if os.path.exists(net_dir):
            for iface in os.listdir(net_dir):
                if os.path.exists(os.path.join(net_dir, iface, 'wireless')):
                    self.interfaces.append(self._get_info(iface))
        
        return self.interfaces
    
    def _get_info(self, name: str) -> Dict:
        info = {'name': name, 'mode': 'Managed', 'status': 'down', 'mac': '', 'vendor': ''}
        
        try:
            with open(f'/sys/class/net/{name}/operstate', 'r') as f:
                info['status'] = f.read().strip()
            
            with open(f'/sys/class/net/{name}/address', 'r') as f:
                info['mac'] = f.read().strip()
                info['vendor'] = self.get_vendor(info['mac'])
            
            result = subprocess.run(['iwconfig', name], capture_output=True, text=True, timeout=5)
            if 'Mode:Monitor' in result.stdout:
                info['mode'] = 'Monitor'
        except:
            pass
        
        return info
    
    def select_interface(self, interfaces: List[Dict] = None) -> Optional[str]:
        interfaces = interfaces or self.interfaces
        
        if not interfaces:
            print(f"{R}No wireless interfaces found!{RESET}")
            return None
        
        print(f"\n{C}Available Interfaces:{RESET}")
        for i, iface in enumerate(interfaces, 1):
            mode_color = M if iface['mode'] == 'Monitor' else W
            status_color = G if iface['status'] == 'up' else R
            print(f"  {i}. {iface['name']} {status_color}[{iface['status']}]{RESET} "
                  f"{mode_color}[{iface['mode']}]{RESET} {iface['mac']} {iface['vendor']}")
        
        try:
            choice = int(input(f"\n{Y}Select interface: {RESET}"))
            if 1 <= choice <= len(interfaces):
                self.selected = interfaces[choice - 1]['name']
                return self.selected
        except (ValueError, IndexError):
            pass
        
        return None
    
    def enable_monitor_mode(self, interface: str = None) -> bool:
        interface = interface or self.selected
        if not interface:
            return False
        
        # Kill interfering processes
        subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], capture_output=True)
        
        # Try airmon-ng
        result = subprocess.run(
            ['sudo', 'airmon-ng', 'start', interface],
            capture_output=True, text=True
        )
        
        match = re.search(r'monitor mode (?:enabled|VIF) on (\S+)', result.stdout)
        if match:
            self.monitor_interface = match.group(1)
            self.selected = self.monitor_interface
            return True
        
        # Manual mode
        for cmd in [
            ['sudo', 'ip', 'link', 'set', interface, 'down'],
            ['sudo', 'iw', 'dev', interface, 'set', 'type', 'monitor'],
            ['sudo', 'ip', 'link', 'set', interface, 'up'],
        ]:
            subprocess.run(cmd, capture_output=True)
        
        if self._verify_monitor(interface):
            self.monitor_interface = interface
            return True
        
        return False
    
    def _verify_monitor(self, interface: str) -> bool:
        try:
            result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
            return 'Mode:Monitor' in result.stdout
        except:
            return False
    
    def disable_monitor_mode(self, interface: str = None) -> bool:
        interface = interface or self.monitor_interface or self.selected
        if not interface:
            return False
        
        subprocess.run(['sudo', 'airmon-ng', 'stop', interface], capture_output=True)
        
        for cmd in [
            ['sudo', 'ip', 'link', 'set', interface, 'down'],
            ['sudo', 'iw', 'dev', interface, 'set', 'type', 'managed'],
            ['sudo', 'ip', 'link', 'set', interface, 'up'],
        ]:
            subprocess.run(cmd, capture_output=True)
        
        subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], capture_output=True)
        
        self.monitor_interface = None
        return True
    
    def set_channel(self, interface: str, channel: int) -> bool:
        try:
            subprocess.run(['sudo', 'iwconfig', interface, 'channel', str(channel)],
                         capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def change_mac(self, interface: str, new_mac: str) -> bool:
        if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', new_mac):
            return False
        
        for cmd in [
            ['sudo', 'ip', 'link', 'set', interface, 'down'],
            ['sudo', 'ip', 'link', 'set', interface, 'address', new_mac],
            ['sudo', 'ip', 'link', 'set', interface, 'up'],
        ]:
            subprocess.run(cmd, capture_output=True)
        
        return True
    
    def random_mac(self, interface: str = None) -> str:
        interface = interface or self.selected
        mac = [random.randint(0x00, 0xff) & 0xfe | 0x02]
        mac += [random.randint(0x00, 0xff) for _ in range(5)]
        new_mac = ':'.join(f'{b:02x}' for b in mac)
        
        if self.change_mac(interface, new_mac):
            return new_mac
        return ""
