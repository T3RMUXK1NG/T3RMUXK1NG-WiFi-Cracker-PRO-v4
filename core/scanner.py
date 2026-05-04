#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T3RMUXK1NG WiFi Cracker PRO v4.0 - Network Scanner Module
Advanced WiFi network discovery with multiple scanning methods
Author: T3rmuxk1ng | Private Release
"""

import os
import re
import sys
import time
import json
import signal
import subprocess
import threading
import queue
import socket
import struct
import fcntl
import select
import hashlib
import random
import datetime
import functools
import itertools
import collections
import typing
from typing import (
    Any, Dict, List, Tuple, Set, Optional, Callable,
    Generator, Iterator, Union, TypeVar, Generic
)
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from collections import defaultdict, deque, Counter, namedtuple
from functools import wraps, lru_cache

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.types import WiFiNetwork, WiFiClient, ScanResult
from utils.logger import Logger
from utils.config import config

logger = Logger('Scanner')


class ScanType(Enum):
    """Scan types"""
    QUICK = auto()
    NORMAL = auto()
    DEEP = auto()
    CONTINUOUS = auto()
    CHANNEL = auto()
    BAND = auto()
    SCAPY = auto()


class ScanMode(Enum):
    """Scan modes"""
    ACTIVE = "active"
    PASSIVE = "passive"
    HYBRID = "hybrid"


class NetworkScanner:
    """
    Advanced WiFi Network Scanner
    
    Features:
    - Multiple scanning backends (airodump, scapy, nmcli)
    - Real-time network discovery
    - Client detection
    - WPS detection
    - Hidden network discovery
    - Band scanning (2.4GHz, 5GHz, 6GHz)
    - Channel hopping
    - Custom filters
    """
    
    # OUI database for vendor lookup
    OUI_DB: Dict[str, str] = {}
    
    # Common default credentials
    DEFAULT_CREDS = {
        'TP-LINK': [('admin', 'admin'), ('admin', 'password')],
        'NETGEAR': [('admin', 'password'), ('admin', 'admin')],
        'D-LINK': [('admin', 'admin'), ('admin', '')],
        'LINKSYS': [('admin', 'admin'), ('', 'admin')],
        'ASUS': [('admin', 'admin'), ('admin', 'password')],
        'CISCO': [('admin', 'admin'), ('cisco', 'cisco')],
        'BELKIN': [('admin', 'admin'), ('', 'admin')],
        'TENDA': [('admin', 'admin'), ('admin', '')],
        'HUAWEI': [('admin', 'admin'), ('user', 'user')],
        'ZTE': [('admin', 'admin'), ('user', 'user')],
        'XIAOMI': [('admin', 'admin'), ('', 'admin')],
    }
    
    # Channel to frequency mapping
    CHANNEL_FREQ = {
        # 2.4 GHz
        **{ch: 2407 + (ch * 5) for ch in range(1, 14)},
        14: 2484,
        # 5 GHz
        **{ch: 5000 + (ch * 5) for ch in [
            36, 40, 44, 48, 52, 56, 60, 64,
            100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144,
            149, 153, 157, 161, 165, 169, 173, 177
        ]},
        # 6 GHz
        **{ch: 5950 + (ch * 5) for ch in range(1, 233)},
    }
    
    def __init__(self, interface: str):
        self.interface = interface
        self.networks: Dict[str, WiFiNetwork] = {}
        self.clients: Dict[str, WiFiClient] = {}
        self.scan_process = None
        self.scanning = False
        self.scan_queue = queue.Queue()
        self.callbacks: List[Callable] = []
        
        # Scan statistics
        self.scan_stats = {
            'start_time': None,
            'end_time': None,
            'packets_captured': 0,
            'networks_found': 0,
            'clients_found': 0,
            'scan_count': 0,
            'total_time': 0.0
        }
        
        # Output directory
        self.output_dir = Path(config.get('general.temp_dir', '/tmp/t3rmuxk1ng_wifi'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load OUI database
        self._load_oui_db()
    
    def _load_oui_db(self):
        """Load OUI database for vendor lookup"""
        if self.OUI_DB:
            return
        
        oui_paths = [
            '/usr/share/ieee-data/oui.txt',
            '/usr/share/wireshark/manuf',
            '/etc/manuf',
            '/usr/share/nmap/nmap-mac-prefixes',
        ]
        
        for path in oui_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', errors='ignore') as f:
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith('#'):
                                continue
                            
                            parts = line.split()
                            if len(parts) >= 2:
                                # Handle different formats
                                mac_part = parts[0].replace(':', '').upper()[:6]
                                vendor = parts[-1].split('#')[0].strip()
                                
                                if len(mac_part) == 6:
                                    self.OUI_DB[mac_part] = vendor
                                    
                    logger.debug(f"Loaded OUI database from {path}")
                    break
                except Exception as e:
                    logger.debug(f"Failed to load OUI from {path}: {e}")
    
    def get_vendor(self, mac: str) -> str:
        """Get vendor from MAC address"""
        prefix = mac.replace(':', '').upper()[:6]
        return self.OUI_DB.get(prefix, 'Unknown')
    
    def get_frequency(self, channel: int) -> int:
        """Convert channel to frequency"""
        return self.CHANNEL_FREQ.get(channel, 0)
    
    def get_band(self, channel: int) -> str:
        """Determine band from channel"""
        if 1 <= channel <= 14:
            return "2.4GHz"
        elif 36 <= channel <= 177:
            return "5GHz"
        elif channel > 177:
            return "6GHz"
        return "Unknown"
    
    def scan(self, duration: int = 30, channel: int = None, 
             mode: ScanMode = ScanMode.ACTIVE) -> List[WiFiNetwork]:
        """
        Scan for WiFi networks
        
        Args:
            duration: Scan duration in seconds
            channel: Specific channel to scan (optional)
            mode: Scan mode
            
        Returns:
            List of discovered networks
        """
        self.scan_stats['start_time'] = datetime.datetime.now()
        self.scan_stats['scan_count'] += 1
        
        output_file = str(self.output_dir / f"scan_{int(time.time())}")
        
        # Build airodump command
        cmd = [
            'sudo', 'airodump-ng', self.interface,
            '-w', output_file,
            '--output-format', 'csv',
            '--write-interval', '1'
        ]
        
        if channel:
            cmd.extend(['-c', str(channel)])
        
        try:
            self.scan_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            self.scanning = True
            
            csv_file = f"{output_file}-01.csv"
            
            # Monitor scan progress
            for elapsed in range(duration):
                if not self.scanning:
                    break
                
                # Parse partial results periodically
                if os.path.exists(csv_file) and elapsed % 3 == 0:
                    self._parse_airodump_csv(csv_file)
                
                # Update display
                if elapsed % 5 == 0:
                    print(f"\r{elapsed}/{duration}s | "
                          f"Networks: {len(self.networks)} | "
                          f"Clients: {len(self.clients)}", end='')
                
                time.sleep(1)
            
            self.scanning = False
            
            # Terminate process
            try:
                self.scan_process.terminate()
                self.scan_process.wait(timeout=5)
            except:
                self.scan_process.kill()
            
            # Final parse
            if os.path.exists(csv_file):
                self._parse_airodump_csv(csv_file)
                
                # Cleanup
                for f in self.output_dir.glob(f"scan_{int(self.scan_stats['start_time'].timestamp())}*"):
                    try:
                        f.unlink()
                    except:
                        pass
            
            self.scan_stats['end_time'] = datetime.datetime.now()
            self.scan_stats['networks_found'] = len(self.networks)
            self.scan_stats['clients_found'] = len(self.clients)
            self.scan_stats['total_time'] += duration
            
            return list(self.networks.values())
            
        except FileNotFoundError:
            logger.warning("airodump-ng not found, using nmcli fallback")
            return self._scan_nmcli()
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            return []
    
    def _parse_airodump_csv(self, csv_file: str):
        """Parse airodump-ng CSV output"""
        try:
            with open(csv_file, 'r', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect sections
                if 'BSSID' in line and 'First time seen' in line:
                    section = 'networks'
                    continue
                elif 'Station MAC' in line:
                    section = 'clients'
                    continue
                
                if section == 'networks':
                    self._parse_network_line(line)
                elif section == 'clients':
                    self._parse_client_line(line)
                    
        except Exception as e:
            logger.debug(f"Parse error: {e}")
    
    def _parse_network_line(self, line: str):
        """Parse a single network line"""
        parts = line.split(',')
        
        if len(parts) < 14:
            return
        
        try:
            bssid = parts[0].strip()
            if not bssid or bssid == 'BSSID':
                return
            
            # Parse fields
            power = int(parts[8].strip()) if parts[8].strip().lstrip('-').isdigit() else -100
            channel_str = parts[3].strip()
            channel = int(channel_str) if channel_str.isdigit() else 0
            essid = parts[13].strip().strip('"') or "[Hidden]"
            
            encryption = parts[5].strip()
            cipher = parts[6].strip()
            auth = parts[7].strip()
            
            # WPS detection
            wps = 'WPS' in line
            wps_locked = 'Locked' in line or 'WPSLock' in line
            
            # WPA3 detection
            wpa3 = 'WPA3' in encryption or 'SAE' in auth
            owe = 'OWE' in encryption
            
            # Get additional info
            frequency = self.get_frequency(channel)
            band = self.get_band(channel)
            vendor = self.get_vendor(bssid)
            clients = int(parts[11].strip()) if parts[11].strip().isdigit() else 0
            
            # Create or update network
            if bssid in self.networks:
                network = self.networks[bssid]
                network.power = power
                network.last_seen = datetime.datetime.now().isoformat()
                network.packets += 1
                if clients > network.clients:
                    network.clients = clients
            else:
                network = WiFiNetwork(
                    bssid=bssid,
                    essid=essid,
                    channel=channel,
                    frequency=frequency,
                    power=power,
                    encryption=encryption,
                    cipher=cipher,
                    auth=auth,
                    wps=wps,
                    wps_locked=wps_locked,
                    vendor=vendor,
                    clients=clients,
                    hidden=essid == "[Hidden]",
                    wpa3=wpa3,
                    owe=owe
                )
                self.networks[bssid] = network
                
                # Notify callbacks
                for callback in self.callbacks:
                    try:
                        callback(network)
                    except:
                        pass
        
        except (ValueError, IndexError) as e:
            pass
    
    def _parse_client_line(self, line: str):
        """Parse a single client line"""
        parts = line.split(',')
        
        if len(parts) < 6:
            return
        
        try:
            mac = parts[0].strip()
            if not mac or mac == 'Station MAC':
                return
            
            bssid = parts[5].strip() if len(parts) > 5 else ""
            power = int(parts[3].strip()) if parts[3].strip().lstrip('-').isdigit() else -100
            packets = int(parts[4].strip()) if parts[4].strip().isdigit() else 0
            
            vendor = self.get_vendor(mac)
            
            if mac not in self.clients:
                client = WiFiClient(
                    mac=mac,
                    bssid=bssid,
                    power=power,
                    packets=packets,
                    vendor=vendor
                )
                self.clients[mac] = client
            else:
                client = self.clients[mac]
                client.power = power
                client.packets += packets
                if bssid:
                    client.bssid = bssid
                
        except (ValueError, IndexError):
            pass
    
    def _scan_nmcli(self) -> List[WiFiNetwork]:
        """Fallback scan using nmcli"""
        networks = []
        
        try:
            result = subprocess.run(
                ['nmcli', '-t', '-f', 
                 'BSSID,SSID,SIGNAL,CHAN,SECURITY,WPS',
                 'dev', 'wifi', 'list'],
                capture_output=True, text=True, timeout=30
            )
            
            for line in result.stdout.strip().split('\n'):
                parts = line.split(':')
                if len(parts) >= 5:
                    bssid = parts[0]
                    essid = parts[1] or "[Hidden]"
                    signal = int(parts[2]) if parts[2].isdigit() else 0
                    channel = int(parts[3]) if parts[3].isdigit() else 0
                    encryption = parts[4] if len(parts) > 4 else ""
                    wps = len(parts) > 5 and parts[5]
                    
                    network = WiFiNetwork(
                        bssid=bssid,
                        essid=essid,
                        channel=channel,
                        frequency=self.get_frequency(channel),
                        power=-100 + signal,
                        encryption=encryption,
                        wps=wps,
                        vendor=self.get_vendor(bssid)
                    )
                    networks.append(network)
                    self.networks[bssid] = network
                    
        except FileNotFoundError:
            logger.error("nmcli not found")
        except Exception as e:
            logger.error(f"nmcli scan error: {e}")
        
        return networks
    
    def scan_continuous(self, callback: Callable = None):
        """Start continuous scanning"""
        if callback:
            self.callbacks.append(callback)
        
        output_file = str(self.output_dir / f"continuous_{int(time.time())}")
        
        cmd = ['sudo', 'airodump-ng', self.interface, '-w', output_file,
               '--output-format', 'csv', '--write-interval', '2']
        
        self.scan_process = subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        self.scanning = True
        
        csv_file = f"{output_file}-01.csv"
        last_size = 0
        
        def monitor():
            nonlocal last_size
            while self.scanning:
                time.sleep(2)
                
                if os.path.exists(csv_file):
                    try:
                        size = os.path.getsize(csv_file)
                        if size != last_size:
                            self._parse_airodump_csv(csv_file)
                            last_size = size
                    except:
                        pass
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        
        logger.info("Continuous scan started. Call stop_scan() to stop.")
    
    def scan_channel(self, channel: int, duration: int = 30) -> List[WiFiNetwork]:
        """Scan specific channel"""
        return self.scan(duration, channel=channel)
    
    def scan_bands(self, bands: List[str] = None, duration_per_band: int = 15) -> List[WiFiNetwork]:
        """Scan multiple bands"""
        bands = bands or ['2.4GHz', '5GHz']
        all_networks = []
        
        # 2.4 GHz channels
        if '2.4GHz' in bands:
            for ch in range(1, 14):
                self.scan_channel(ch, 3)
            all_networks.extend(self.networks.values())
        
        # 5 GHz channels
        if '5GHz' in bands:
            channels_5ghz = [36, 40, 44, 48, 52, 56, 60, 64,
                           100, 104, 108, 112, 116, 120, 124, 128,
                           132, 136, 140, 144, 149, 153, 157, 161, 165]
            
            for ch in channels_5ghz:
                self.scan_channel(ch, 2)
        
        return list(self.networks.values())
    
    def scan_scapy(self, duration: int = 30) -> List[WiFiNetwork]:
        """Scan using scapy"""
        try:
            from scapy.all import Dot11, Dot11Beacon, Dot11Elt, sniff
        except ImportError:
            logger.error("Scapy not available")
            return []
        
        def packet_handler(pkt):
            if pkt.haslayer(Dot11Beacon):
                bssid = pkt[Dot11].addr2
                if bssid in self.networks:
                    return
                
                # Get ESSID
                try:
                    essid = pkt[Dot11Elt].info.decode('utf-8', errors='ignore')
                except:
                    essid = "[Hidden]"
                
                # Get channel
                try:
                    channel = ord(pkt[Dot11Elt:3].info)
                except:
                    channel = 0
                
                # Get encryption
                encryption = "Open"
                cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}")
                if 'privacy' in cap:
                    encryption = "WEP/WPA"
                
                network = WiFiNetwork(
                    bssid=bssid,
                    essid=essid or "[Hidden]",
                    channel=channel,
                    frequency=self.get_frequency(channel),
                    power=-50,
                    encryption=encryption,
                    vendor=self.get_vendor(bssid)
                )
                self.networks[bssid] = network
        
        logger.info(f"Scanning with scapy for {duration}s...")
        sniff(iface=self.interface, prn=packet_handler, timeout=duration)
        
        return list(self.networks.values())
    
    def stop_scan(self):
        """Stop ongoing scan"""
        self.scanning = False
        if self.scan_process:
            try:
                self.scan_process.terminate()
                self.scan_process.wait(timeout=5)
            except:
                self.scan_process.kill()
            self.scan_process = None
    
    def get_network(self, bssid: str) -> Optional[WiFiNetwork]:
        """Get network by BSSID"""
        return self.networks.get(bssid)
    
    def get_networks_by_essid(self, essid: str) -> List[WiFiNetwork]:
        """Get networks by ESSID"""
        return [n for n in self.networks.values() if n.essid == essid]
    
    def get_clients(self, bssid: str = None) -> List[WiFiClient]:
        """Get clients, optionally filtered by BSSID"""
        if bssid:
            return [c for c in self.clients.values() if c.bssid == bssid]
        return list(self.clients.values())
    
    def suggest_attacks(self, bssid: str) -> List[Dict]:
        """Suggest possible attacks for a network"""
        network = self.networks.get(bssid)
        if not network:
            return []
        
        attacks = []
        
        # WPS attacks
        if network.wps and not network.wps_locked:
            attacks.append({
                'type': 'wps_pixie',
                'name': 'WPS Pixie Dust',
                'difficulty': 'easy',
                'success_rate': 'high',
                'time': '1-60s'
            })
            attacks.append({
                'type': 'wps_brute',
                'name': 'WPS PIN Brute Force',
                'difficulty': 'medium',
                'success_rate': 'medium',
                'time': 'hours'
            })
        
        # PMKID
        if 'WPA' in network.encryption:
            attacks.append({
                'type': 'pmkid',
                'name': 'PMKID Attack',
                'difficulty': 'medium',
                'success_rate': 'high',
                'time': 'minutes'
            })
        
        # Handshake
        if 'WPA' in network.encryption and network.clients > 0:
            attacks.append({
                'type': 'handshake',
                'name': 'Handshake Capture',
                'difficulty': 'medium',
                'success_rate': 'varies',
                'time': 'minutes'
            })
        
        # Evil Twin
        attacks.append({
            'type': 'evil_twin',
            'name': 'Evil Twin',
            'difficulty': 'medium',
            'success_rate': 'high',
            'time': 'varies'
        })
        
        return attacks
    
    def export_results(self, format: str = 'json', output_file: str = None) -> str:
        """Export scan results"""
        data = {
            'scan_time': self.scan_stats['start_time'].isoformat() if self.scan_stats['start_time'] else None,
            'networks_count': len(self.networks),
            'clients_count': len(self.clients),
            'networks': [n.to_dict() for n in self.networks.values()],
            'clients': [c.to_dict() for c in self.clients.values()]
        }
        
        output_file = output_file or str(self.output_dir / f"scan_results_{int(time.time())}.{format}")
        
        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        elif format == 'csv':
            import csv
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=WiFiNetwork.__dataclass_fields__.keys())
                writer.writeheader()
                for n in self.networks.values():
                    writer.writerow(n.to_dict())
        
        return output_file
    
    def get_stats(self) -> Dict:
        """Get scan statistics"""
        return {
            **self.scan_stats,
            'networks_count': len(self.networks),
            'clients_count': len(self.clients),
            'crackable': sum(1 for n in self.networks.values() if n.is_crackable),
            'wps_vulnerable': sum(1 for n in self.networks.values() if n.wps and not n.wps_locked),
            'open_networks': sum(1 for n in self.networks.values() if 'Open' in n.encryption),
            'wpa3_networks': sum(1 for n in self.networks.values() if n.wpa3),
        }


# Standalone CLI
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='WiFi Network Scanner')
    parser.add_argument('interface', help='Wireless interface')
    parser.add_argument('-d', '--duration', type=int, default=30, help='Scan duration')
    parser.add_argument('-c', '--channel', type=int, help='Channel to scan')
    parser.add_argument('-o', '--output', help='Output file')
    
    args = parser.parse_args()
    
    scanner = NetworkScanner(args.interface)
    print(f"Scanning for {args.duration} seconds...")
    
    networks = scanner.scan(args.duration, args.channel)
    
    print(f"\nFound {len(networks)} networks:")
    for n in networks:
        print(f"  {n.essid} ({n.bssid}) - {n.encryption} - Ch:{n.channel}")
    
    if args.output:
        scanner.export_results('json', args.output)
