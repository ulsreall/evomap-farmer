#!/usr/bin/env python3
"""EvoMap heartbeat — keep node alive, report status."""
import json
import os
import sys
import time
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    os.system("pip install -q requests")
    import requests

NODE_ID = "node_7665be8b29add3cf"
NODE_SECRET = "7636775949338ef02044c16ce235b7ca999846488891aed87504502aa9b40e55"
API_BASE = "https://evomap.ai/a2a"


def heartbeat():
    payload = {
        "node_id": NODE_ID,
        "node_secret": NODE_SECRET,
        "ts": int(time.time()),
    }
    try:
        r = requests.post(f"{API_BASE}/heartbeat", json=payload, timeout=15)
        data = r.json()
        status = data.get("status", "error")
        balance = data.get("credit_balance", "?")
        node_status = data.get("node_status", "?")
        available = len(data.get("available_work", []))
        survival = data.get("survival_status", "?")

        # Check for force update
        fu = data.get("force_update", {})
        if fu:
            print(f"[EVOMAP] ⚠️ Force update: {fu.get('reason', 'unknown')}")

        print(f"[EVOMAP] ❤️ {status} | balance={balance} | status={node_status} | survival={survival} | tasks={available}")

        # Detail for debugging
        if status == "ok":
            now = datetime.now(timezone.utc).isoformat()
            report = {
                "ts": now,
                "balance": balance,
                "status": node_status,
                "survival": survival,
                "tasks_available": available,
                "claimed": data.get("claimed", False),
            }
            os.makedirs("/tmp/.evomap", exist_ok=True)
            with open("/tmp/.evomap/last_heartbeat.json", "w") as f:
                json.dump(report, f)
            return True, data
        return False, data
    except Exception as e:
        print(f"[EVOMAP] ❌ Heartbeat failed: {e}")
        return False, {"error": str(e)}


if __name__ == "__main__":
    ok, data = heartbeat()
    sys.exit(0 if ok else 1)