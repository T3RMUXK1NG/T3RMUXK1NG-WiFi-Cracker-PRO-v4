#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - Logger Utility"""

import os
import sys
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
W = '\033[97m'
RESET = '\033[0m'


class Logger:
    """Advanced Logging System"""
    
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    
    def __init__(self, name: str = 'RSWiFi', log_file: str = None, level: str = 'INFO'):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.LEVELS.get(level, logging.INFO))
        
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(
            f'%(asctime)s [{C}%(levelname)s{RESET}] %(message)s', datefmt='%H:%M:%S'
        ))
        self.logger.addHandler(ch)
        
        # File handler
        self.log_file = log_file or str(PROJECT_ROOT / 'logs' / f'{name.lower()}.log')
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        
        rfh = logging.handlers.RotatingFileHandler(
            self.log_file, maxBytes=10*1024*1024, backupCount=5
        )
        rfh.setLevel(logging.DEBUG)
        rfh.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(rfh)
    
    def debug(self, msg: str): self.logger.debug(msg)
    def info(self, msg: str): self.logger.info(msg)
    def warning(self, msg: str): self.logger.warning(msg)
    def error(self, msg: str): self.logger.error(msg)
    def critical(self, msg: str): self.logger.critical(msg)
    def success(self, msg: str): self.logger.info(f"{G}✓{RESET} {msg}")
    def fail(self, msg: str): self.logger.error(f"{R}✗{RESET} {msg}")
    def target(self, msg: str): self.logger.info(f"{C}→{RESET} {msg}")
    
    def section(self, title: str):
        print(f"\n{M}{'═' * 20} {title} {'═' * 20}{RESET}\n")
