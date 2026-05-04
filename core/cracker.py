#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T3RMUXK1NG WiFi Cracker PRO v4.0 - Password Cracker Module"""

import os
import re
import sys
import time
import json
import subprocess
import threading
import hashlib
import itertools
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Generator, Callable
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.types import CrackResult
from utils.logger import Logger
from utils.config import config

logger = Logger('Cracker')


class PasswordCracker:
    """Advanced Multi-Method Password Cracker"""
    
    # Common patterns
    PATTERNS = {
        'numeric': r'^\d+$',
        'alpha_lower': r'^[a-z]+$',
        'alpha_upper': r'^[A-Z]+$',
        'alphanumeric': r'^[a-zA-Z0-9]+$',
    }
    
    def __init__(self):
        self.results: List[CrackResult] = []
        self.stop_flag = False
        self.current_attempt = 0
        self.start_time = None
        self.progress_callback: Optional[Callable] = None
        self.stats = {
            'total_cracked': 0,
            'total_failed': 0,
            'total_time': 0.0,
            'total_attempts': 0
        }
        self.output_dir = Path(config.get('general.output_dir', '/tmp/t3rmuxk1ng_wifi/output'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def crack(self, cap_file: str, wordlist: str, method: str = "dictionary",
              rules: str = None) -> CrackResult:
        """Main cracking dispatcher"""
        start_time = time.time()
        
        if not os.path.exists(cap_file):
            return CrackResult(success=False, target=cap_file, error="Capture file not found")
        
        methods = {
            'dictionary': self._crack_dictionary,
            'brute': self._crack_brute,
            'rule': self._crack_rule,
            'combo': self._crack_combo,
            'hybrid': self._crack_hybrid,
            'mask': self._crack_mask,
            'incremental': self._crack_incremental,
        }
        
        cracker = methods.get(method, self._crack_dictionary)
        result = cracker(cap_file, wordlist, rules=rules)
        
        result.time_taken = time.time() - start_time
        self.results.append(result)
        self._update_stats(result)
        
        return result
    
    def _crack_dictionary(self, cap_file: str, wordlist: str, **kwargs) -> CrackResult:
        """Dictionary attack using aircrack-ng"""
        if not os.path.exists(wordlist):
            return CrackResult(success=False, target=cap_file, error="Wordlist not found")
        
        try:
            cmd = ['aircrack-ng', '-w', wordlist, cap_file]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, _ = process.communicate(timeout=3600)
            
            if 'KEY FOUND!' in output:
                match = re.search(r'\[\s*([^\]]+)\s*\]', output.split('KEY FOUND!')[1])
                if match:
                    return CrackResult(
                        success=True, target=cap_file,
                        password=match.group(1).strip(),
                        method='dictionary', wordlist=wordlist
                    )
            
            return CrackResult(success=False, target=cap_file, method='dictionary',
                              wordlist=wordlist, error="Password not in wordlist")
        
        except subprocess.TimeoutExpired:
            return CrackResult(success=False, target=cap_file, error="Timeout")
        except FileNotFoundError:
            return CrackResult(success=False, target=cap_file, error="aircrack-ng not found")
        except Exception as e:
            return CrackResult(success=False, target=cap_file, error=str(e))
    
    def _crack_brute(self, cap_file: str, wordlist: str = None,
                     charset: str = None, max_len: int = 8, **kwargs) -> CrackResult:
        """Brute force attack"""
        if not charset:
            charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
        
        temp_wl = f"/tmp/brute_{int(time.time())}.txt"
        attempts = 0
        start_time = time.time()
        
        with open(temp_wl, 'w') as f:
            for length in range(1, max_len + 1):
                for combo in itertools.product(charset, repeat=length):
                    if self.stop_flag:
                        break
                    f.write(''.join(combo) + '\n')
                    attempts += 1
                    
                    if attempts % 100000 == 0:
                        f.flush()
                        result = self._crack_dictionary(cap_file, temp_wl)
                        if result.success:
                            os.remove(temp_wl)
                            return result
                        open(temp_wl, 'w').close()
        
        result = self._crack_dictionary(cap_file, temp_wl)
        os.remove(temp_wl)
        result.method = 'brute'
        result.attempts = attempts
        return result
    
    def _crack_rule(self, cap_file: str, wordlist: str, rules: str = None, **kwargs) -> CrackResult:
        """Rule-based attack"""
        if not os.path.exists(wordlist):
            return CrackResult(success=False, target=cap_file, error="Wordlist not found")
        
        temp_wl = f"/tmp/rule_{int(time.time())}.txt"
        passwords = set()
        
        with open(wordlist, 'r') as f:
            for line in f:
                pwd = line.strip()
                if not pwd: continue
                
                passwords.add(pwd)
                passwords.add(pwd.upper())
                passwords.add(pwd.lower())
                passwords.add(pwd.capitalize())
                passwords.add(pwd + '1')
                passwords.add(pwd + '123')
                passwords.add(pwd + '!')
                passwords.add(pwd[::-1])
                passwords.add(pwd.replace('a', '@').replace('e', '3').replace('i', '1'))
        
        with open(temp_wl, 'w') as f:
            for p in passwords:
                f.write(p + '\n')
        
        result = self._crack_dictionary(cap_file, temp_wl)
        os.remove(temp_wl)
        result.method = 'rule'
        return result
    
    def _crack_combo(self, cap_file: str, wordlist: str, **kwargs) -> CrackResult:
        """Combinator attack"""
        with open(wordlist, 'r') as f:
            words = [l.strip() for l in f if l.strip()][:1000]
        
        temp_wl = f"/tmp/combo_{int(time.time())}.txt"
        mid = len(words) // 2
        
        with open(temp_wl, 'w') as f:
            for w1 in words[:mid]:
                for w2 in words[mid:]:
                    f.write(w1 + w2 + '\n')
                    f.write(w2 + w1 + '\n')
        
        result = self._crack_dictionary(cap_file, temp_wl)
        os.remove(temp_wl)
        result.method = 'combo'
        return result
    
    def _crack_hybrid(self, cap_file: str, wordlist: str, **kwargs) -> CrackResult:
        """Hybrid attack"""
        with open(wordlist, 'r') as f:
            words = [l.strip() for l in f if l.strip()][:1000]
        
        temp_wl = f"/tmp/hybrid_{int(time.time())}.txt"
        
        with open(temp_wl, 'w') as f:
            for word in words:
                f.write(word + '\n')
                for i in range(1000):
                    f.write(f"{word}{i}\n")
        
        result = self._crack_dictionary(cap_file, temp_wl)
        os.remove(temp_wl)
        result.method = 'hybrid'
        return result
    
    def _crack_mask(self, cap_file: str, wordlist: str = None,
                    mask: str = "?l?l?l?l?l?l?l?l", **kwargs) -> CrackResult:
        """Mask attack"""
        mask_chars = {
            '?l': 'abcdefghijklmnopqrstuvwxyz',
            '?u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            '?d': '0123456789',
            '?s': '!@#$%^&*',
            '?a': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        }
        
        charsets = []
        i = 0
        while i < len(mask):
            if mask[i] == '?' and i + 1 < len(mask):
                charsets.append(mask_chars.get(mask[i:i+2], ''))
                i += 2
            else:
                charsets.append(mask[i])
                i += 1
        
        temp_wl = f"/tmp/mask_{int(time.time())}.txt"
        
        with open(temp_wl, 'w') as f:
            for combo in itertools.product(*charsets):
                if self.stop_flag: break
                f.write(''.join(combo) + '\n')
        
        result = self._crack_dictionary(cap_file, temp_wl)
        os.remove(temp_wl)
        result.method = 'mask'
        return result
    
    def _crack_incremental(self, cap_file: str, wordlist: str = None, **kwargs) -> CrackResult:
        """Incremental brute force"""
        charsets = ['0123456789', 'abcdefghijklmnopqrstuvwxyz', 
                    'abcdefghijklmnopqrstuvwxyz0123456789']
        
        for charset in charsets:
            result = self._crack_brute(cap_file, charset=charset, max_len=8)
            if result.success:
                result.method = 'incremental'
                return result
            if self.stop_flag: break
        
        return CrackResult(success=False, target=cap_file, method='incremental',
                          error="Password not found")
    
    def crack_hashcat(self, cap_file: str, wordlist: str, 
                      hash_mode: int = 22000, rules: str = None) -> CrackResult:
        """GPU cracking with hashcat"""
        # Convert to hccapx
        hccapx = cap_file.replace('.cap', '.hccapx')
        try:
            subprocess.run(['aircrack-ng', '-J', hccapx.replace('.hccapx', ''), cap_file],
                          capture_output=True)
        except:
            pass
        
        if not os.path.exists(hccapx):
            return CrackResult(success=False, target=cap_file, error="Conversion failed")
        
        try:
            cmd = ['hashcat', '-m', str(hash_mode), hccapx, wordlist, '--force']
            if rules: cmd.extend(['-r', rules])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
            
            if 'Cracked' in result.stdout or result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if hccapx in line and ':' in line:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            return CrackResult(success=True, target=cap_file,
                                              password=parts[-1].strip(), method='hashcat')
            
            return CrackResult(success=False, target=cap_file, method='hashcat',
                              error="Password not found")
        
        except FileNotFoundError:
            return CrackResult(success=False, target=cap_file, error="hashcat not found")
        except Exception as e:
            return CrackResult(success=False, target=cap_file, error=str(e))
    
    def crack_pmkid(self, pmkid_file: str, wordlist: str = None) -> CrackResult:
        """Crack PMKID capture"""
        wordlist = wordlist or '/usr/share/wordlists/rockyou.txt'
        return self.crack_hashcat(pmkid_file, wordlist, hash_mode=16800)
    
    def stop(self): self.stop_flag = True
    def _update_stats(self, result: CrackResult):
        if result.success: self.stats['total_cracked'] += 1
        else: self.stats['total_failed'] += 1
        self.stats['total_time'] += result.time_taken
    def get_stats(self) -> Dict: return self.stats.copy()
    def get_results(self) -> List[CrackResult]: return self.results.copy()
