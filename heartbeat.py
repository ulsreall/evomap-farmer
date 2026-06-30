#!/usr/bin/env python3
"""
EvoMap Heartbeat Loop — Keep node alive and log status.

Usage:
    python3 heartbeat.py              # Run forever (tiap 5 menit)
    python3 heartbeat.py --once       # Kirim heartbeat sekali
    python3 heartbeat.py --interval 10  # Custom interval (menit)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests")
    sys.exit(1)

API_BASE = "https://evomap.ai/a2a"

def load_credentials():
    evomap_dir = os.path.expanduser("~/.evomap")
    node_id_path = os.path.join(evomap_dir, "node_id")
    secret_path = os.path.join(evomap_dir, "node_secret")
    
    if not os.path.exists(node_id_path) or not os.path.exists(secret_path):
        print("Error: Node not registered. Run: python3 setup/register_node.py")
        sys.exit(1)
    
    with open(node_id_path) as f:
        node_id = f.read().strip()
    with open(secret_path) as f:
        secret = open("/root/evomap-farmer/heartbeat.py").read()
    
    return node_id, secret

def send_heartbeat(node_id, secret):
    headers = {
        "Authorization": "Bearer " + secret,
        "Content-Type": "application/json"
    }
    
    try:
        r = requests.post(
            f"{API_BASE}/heartbeat",
            headers=headers,
            json={"node_id": node_id, "status": "alive"},
            timeout=15
        )
        data = r.json()
        
        ts = datetime.now().strftime("%H:%M:%S")
        status = data.get("node_status", "?")
        credits = data.get("onboarding", {}).get("account_credits", "?")
        rep = data.get("onboarding", {}).get("reputation", "?")
        tasks = len(data.get("available_work", []))
        
        print(f"[{ts}] Status: {status} | Credits: {credits} | Rep: {rep} | Tasks: {tasks}")
        return data
    except Exception as e:
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="EvoMap Heartbeat")
    parser.add_argument("--once", action="store_true", help="Send once and exit")
    parser.add_argument("--interval", type=int, default=5, help="Interval in minutes (default: 5)")
    args = parser.parse_args()
    
    node_id, secret = load_credentials()
    print(f"Node: {node_id}")
    print(f"Interval: {args.interval} minutes")
    print()
    
    while True:
        send_heartbeat(node_id, secret)
        
        if args.once:
            break
        
        time.sleep(args.interval * 60)

if __name__ == "__main__":
    main()
