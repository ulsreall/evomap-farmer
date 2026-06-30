#!/usr/bin/env python3
"""
Register a new EvoMap node via A2A protocol (captcha-free!).

Usage:
    python3 register_node.py

This will:
1. Register a new node on EvoMap
2. Save credentials to ~/.evomap/
3. Give you a claim URL to bind the node to your account
"""

import hashlib
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests")
    sys.exit(1)

API_BASE = "https://evomap.ai/a2a"

def register():
    """Register a new node via A2A hello endpoint"""
    print("=" * 50)
    print("  EvoMap Node Registration (A2A Protocol)")
    print("=" * 50)
    print()
    
    # Check if already registered
    evomap_dir = os.path.expanduser("~/.evomap")
    node_id_path = os.path.join(evomap_dir, "node_id")
    secret_path = os.path.join(evomap_dir, "node_secret")
    
    if os.path.exists(node_id_path) and os.path.exists(secret_path):
        with open(node_id_path) as f:
            existing_id = f.read().strip()
        print(f"Node already registered: {existing_id}")
        print(f"Credentials at: {evomap_dir}/")
        print()
        resp = input("Register new node anyway? (y/N): ").strip().lower()
        if resp != "y":
            print("Aborted.")
            return
    
    # Register via A2A hello
    print("\nRegistering node...")
    
    payload = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "hello",
        "message_id": "msg_" + str(int(time.time() * 1000)),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "payload": {
            "capabilities": {},
            "model": "python-farmer",
            "name": "EvoMap Farmer",
            "env_fingerprint": {
                "platform": "linux",
                "arch": "x64"
            }
        }
    }
    
    try:
        r = requests.post(
            f"{API_BASE}/hello",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        data = r.json()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    if r.status_code != 200:
        print(f"Registration failed: {data}")
        sys.exit(1)
    
    # Extract credentials
    node_id = data.get("your_node_id")
    node_secret = data.get("node_secret")
    claim_url = data.get("claim_url")
    claim_code = data.get("claim_code")
    
    if not node_id or not node_secret:
        print(f"Unexpected response: {json.dumps(data, indent=2)}")
        sys.exit(1)
    
    # Save credentials
    os.makedirs(evomap_dir, exist_ok=True)
    
    with open(node_id_path, "w") as f:
        f.write(node_id)
    with open(secret_path, "w") as f:
        f.write(node_secret)
    
    # Set permissions (secret should be private)
    os.chmod(secret_path, 0o600)
    os.chmod(node_id_path, 0o600)
    
    print()
    print("=" * 50)
    print("  Node Registered Successfully!")
    print("=" * 50)
    print()
    print(f"  Node ID:     {node_id}")
    print(f"  Secret:      {node_secret[:8]}...{node_secret[-8:]}")
    print(f"  Credentials: {evomap_dir}/")
    print()
    
    if claim_url:
        print("  IMPORTANT: Open this URL in your browser to bind")
        print("  the node to your EvoMap account:")
        print()
        print(f"  {claim_url}")
        print()
        if claim_code:
            print(f"  Claim code: {claim_code}")
            print()
    
    print("  Next steps:")
    print("  1. Open the claim URL above in your browser")
    print("  2. Login to EvoMap and bind the node")
    print("  3. Run: python3 worker.py --once")
    print("  4. If working, run: python3 worker.py")
    print()

if __name__ == "__main__":
    register()
