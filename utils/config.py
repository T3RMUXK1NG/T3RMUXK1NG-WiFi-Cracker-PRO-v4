#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - Configuration Utility"""

import os
import json
import secrets
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).parent.parent.parent

class Config:
    """Configuration Manager"""
    
    DEFAULTS = {
        'general': {
            'interface': 'wlan0',
            'auto_detect': True,
            'log_level': 'INFO',
            'log_file': 'logs/t3rmuxk1ng_wifi.log',
            'output_dir': 'output',
            'temp_dir': '/tmp/t3rmuxk1ng_wifi',
            'colors': True,
            'language': 'en',
        },
        'scanning': {
            'default_duration': 30,
            'channel_hop': True,
            'scan_bands': ['2.4GHz', '5GHz'],
            'min_signal': -90,
        },
        'capture': {
            'default_duration': 120,
            'deauth_packets': 10,
            'capture_timeout': 300,
        },
        'cracking': {
            'default_method': 'dictionary',
            'default_wordlist': '/usr/share/wordlists/rockyou.txt',
            'use_gpu': True,
        },
        'network': {
            'gateway': '10.0.0.1',
            'dhcp_start': '10.0.0.2',
            'dhcp_end': '10.0.0.100',
            'http_port': 80,
            'api_port': 8080,
        },
        'dashboard': {
            'enabled': True,
            'port': 5000,
            'host': '0.0.0.0',
            'secret_key': secrets.token_hex(32),
        },
    }
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.config_file = str(PROJECT_ROOT / 'config' / 'config.json')
        self.config = self.DEFAULTS.copy()
        self.load()
    
    def load(self) -> bool:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    self._merge(loaded)
                return True
        except:
            pass
        return False
    
    def save(self) -> bool:
        try:
            Path(self.config_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except:
            return False
    
    def _merge(self, loaded: Dict):
        for section, values in loaded.items():
            if section in self.config and isinstance(values, dict):
                self.config[section].update(values)
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any, save: bool = True):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        if save:
            self.save()
    
    def get_section(self, section: str) -> Dict:
        return self.config.get(section, {}).copy()
    
    def reset(self, section: str = None):
        if section:
            self.config[section] = self.DEFAULTS.get(section, {})
        else:
            self.config = self.DEFAULTS.copy()
        self.save()


# Global config instance
config = Config()
