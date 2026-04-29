#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - Wordlist Generator Utility"""

import os
import sys
import itertools
import random
from datetime import datetime
from typing import Dict, List, Optional, Generator
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent


class WordlistGenerator:
    """Advanced Password Wordlist Generator"""
    
    COMMON_BASES = [
        'password', 'admin', 'user', 'guest', 'root', 'wifi', 'router',
        'network', 'internet', 'home', 'office', 'company', 'demo', 'test',
    ]
    
    SUFFIXES = ['', '1', '12', '123', '1234', '12345', '!', '@', '#', '!123', '@123']
    YEARS = list(range(1990, datetime.now().year + 2))
    
    def __init__(self):
        self.output_dir = PROJECT_ROOT / 'wordlists'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.stats = {'generated': 0, 'total_passwords': 0}
    
    def from_essid(self, essid: str, output_path: str = None, variations: bool = True) -> str:
        """Generate wordlist from ESSID"""
        passwords = set()
        
        passwords.add(essid)
        passwords.add(essid.lower())
        passwords.add(essid.upper())
        
        if variations:
            for i in range(10000):
                passwords.add(f"{essid}{i}")
            
            for year in self.YEARS:
                passwords.add(f"{essid}{year}")
            
            for suffix in self.SUFFIXES:
                passwords.add(f"{essid}{suffix}")
        
        output_path = output_path or str(self.output_dir / f"{essid}.txt")
        self._write(passwords, output_path)
        return output_path
    
    def common(self, output_path: str = None, top: int = 100000) -> str:
        """Generate common passwords wordlist"""
        passwords = set()
        
        for base in self.COMMON_BASES:
            passwords.add(base)
            for i in range(100):
                passwords.add(f"{base}{i}")
            for year in self.YEARS:
                passwords.add(f"{base}{year}")
        
        for i in range(100000):
            passwords.add(str(i))
        
        passwords = set(list(passwords)[:top])
        
        output_path = output_path or str(self.output_dir / 'common.txt')
        self._write(passwords, output_path)
        return output_path
    
    def mega(self, output_path: str = None) -> str:
        """Generate mega wordlist"""
        passwords = set()
        
        for base in self.COMMON_BASES:
            for i in range(10000):
                passwords.add(f"{base}{i}")
            for year in self.YEARS:
                passwords.add(f"{base}{year}")
        
        for i in range(1000000):
            passwords.add(str(i))
        
        output_path = output_path or str(self.output_dir / 'mega.txt')
        self._write(passwords, output_path)
        return output_path
    
    def _write(self, passwords: set, output_path: str):
        with open(output_path, 'w') as f:
            for pwd in sorted(passwords):
                f.write(pwd + '\n')
        
        self.stats['generated'] += 1
        self.stats['total_passwords'] += len(passwords)
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
