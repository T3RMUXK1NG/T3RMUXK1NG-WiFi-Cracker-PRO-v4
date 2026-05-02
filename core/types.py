#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - Type Definitions"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json

@dataclass
class WiFiNetwork:
    """WiFi Network Data Structure"""
    bssid: str
    essid: str = ""
    channel: int = 0
    frequency: int = 0
    power: int = -100
    encryption: str = ""
    cipher: str = ""
    auth: str = ""
    wps: bool = False
    wps_locked: bool = False
    wps_version: str = ""
    wps_pin: str = ""
    vendor: str = ""
    clients: int = 0
    hidden: bool = False
    wpa3: bool = False
    owe: bool = False
    mesh: bool = False
    beacon_interval: int = 100
    data_rate: float = 0.0
    packets: int = 0
    first_seen: str = ""
    last_seen: str = ""
    notes: str = ""
    
    def __post_init__(self):
        if not self.first_seen:
            self.first_seen = datetime.now().isoformat()
        self.last_seen = datetime.now().isoformat()
    
    @property
    def band(self) -> str:
        if 1 <= self.channel <= 14: return "2.4GHz"
        elif 36 <= self.channel <= 177: return "5GHz"
        return "Unknown"
    
    @property
    def is_crackable(self) -> bool:
        if self.wps and not self.wps_locked: return True
        if 'WPA' in self.encryption or 'WEP' in self.encryption: return True
        return False
    
    @property
    def security_score(self) -> int:
        score = 1
        if 'WPA3' in self.encryption: score = 10
        elif 'WPA2' in self.encryption: score = 8
        elif 'WPA' in self.encryption: score = 6
        elif 'WEP' in self.encryption: score = 2
        if self.wps and not self.wps_locked: score = max(1, score - 3)
        return score
    
    def to_dict(self) -> Dict: return {
        'bssid': self.bssid, 'essid': self.essid, 'channel': self.channel,
        'frequency': self.frequency, 'band': self.band, 'power': self.power,
        'encryption': self.encryption, 'cipher': self.cipher, 'auth': self.auth,
        'wps': self.wps, 'wps_locked': self.wps_locked, 'vendor': self.vendor,
        'clients': self.clients, 'hidden': self.hidden, 'wpa3': self.wpa3,
        'security_score': self.security_score, 'is_crackable': self.is_crackable
    }

@dataclass
class WiFiClient:
    """WiFi Client Data Structure"""
    mac: str
    bssid: str = ""
    power: int = -100
    packets: int = 0
    vendor: str = ""
    probe_requests: List[str] = field(default_factory=list)
    first_seen: str = ""
    last_seen: str = ""
    
    def __post_init__(self):
        if not self.first_seen: self.first_seen = datetime.now().isoformat()
        self.last_seen = datetime.now().isoformat()
    
    def to_dict(self) -> Dict: return {
        'mac': self.mac, 'bssid': self.bssid, 'power': self.power,
        'packets': self.packets, 'vendor': self.vendor,
        'probe_requests': self.probe_requests, 'first_seen': self.first_seen
    }

@dataclass
class ScanResult:
    success: bool
    networks: List[WiFiNetwork] = field(default_factory=list)
    clients: List[WiFiClient] = field(default_factory=list)
    duration: float = 0.0
    error: str = ""

@dataclass
class CaptureResult:
    success: bool
    bssid: str
    essid: str = ""
    cap_file: str = ""
    handshake_type: str = ""
    packets_captured: int = 0
    time_taken: float = 0.0
    error: str = ""

@dataclass
class CrackResult:
    success: bool
    target: str
    password: str = ""
    method: str = ""
    wordlist: str = ""
    time_taken: float = 0.0
    attempts: int = 0
    speed: float = 0.0
    error: str = ""

@dataclass
class AttackResult:
    success: bool
    attack_type: str
    target: str
    password: str = ""
    cap_file: str = ""
    time_taken: float = 0.0
    error: str = ""
    details: Dict = field(default_factory=dict)
