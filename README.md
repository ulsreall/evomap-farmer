# 🌾 EvoMap Credit Farmer

> Otomatis farming credit EvoMap — claim task, solve, submit, repeat.

## Apa itu EvoMap?

[EvoMap](https://evomap.ai) adalah marketplace AI agent dimana agent bisa:
- **Publish** knowledge assets (Gene + Capsule bundles)
- **Claim & solve** bounty tasks
- **Earn credits** dari setiap aktivitas

Credits bisa dipake buat fetch asset lain, post bounty, atau fitur premium.

## Cara Kerja

```
┌─────────────────────────────────────────────┐
│            EvoMap Auto-Worker               │
├─────────────────────────────────────────────┤
│  1. Heartbeat (keep node alive)             │
│  2. Fetch available tasks                   │
│  3. Claim task (bounty first)               │
│  4. Generate solution bundle                │
│  5. Publish to EvoMap                       │
│  6. Submit solution to task                 │
│  7. Repeat setiap 1 jam                     │
└─────────────────────────────────────────────┘
```

## Quick Start

### 1. Register EvoMap Node

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/evomap-farmer.git
cd evomap-farmer

# Register node (captcha-free via A2A protocol)
python3 setup/register_node.py
```

Script akan:
1. Register node baru via A2A protocol (ga perlu captcha!)
2. Simpan `node_id` dan `node_secret` ke `~/.evomap/`
3. Kasih `claim_url` — **buka di browser** buat bind ke akun EvoMap

### 2. Bind Node ke Akun

Buka URL yang dikasih script register di browser. Login ke EvoMap. Node lo sekarang terikat ke akun.

### 3. Jalankan Auto-Worker

```bash
# Test run sekali
python3 worker.py --once

# Run terus-terusan (tiap 1 jam)
python3 worker.py

# Run dengan custom interval (menit)
python3 worker.py --interval 30
```

### 4. (Opsional) Setup sebagai Systemd Service

```bash
sudo cp setup/evomap-worker.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable evomap-worker
sudo systemctl start evomap-worker

# Cek status
sudo systemctl status evomap-worker

# Cek log
journalctl -u evomap-worker -f
```

## File Structure

```
evomap-farmer/
├── README.md              # Ini
├── worker.py              # Auto-worker utama
├── publisher.py           # Batch publisher (publish banyak asset)
├── heartbeat.py           # Keep-alive heartbeat loop
├── config.json            # Konfigurasi (auto-generated)
├── setup/
│   ├── register_node.py   # Script registrasi node
│   └── evomap-worker.service  # Systemd service file
└── logs/
    └── worker.log         # Log file
```

## Earning Methods

| Method | Credits | Notes |
|--------|---------|-------|
| **Task completion** | 5-30/task | Claim → Solve → Submit |
| **Asset accepted** | +20/asset | Published & promoted |
| **Asset reused** | +5/fetch | Agent lain fetch asset kita |
| **Heartbeat** | passive | Keep node alive |
| **Daily cap** | 500/day | Free plan limit |

## Tips Maximize Earnings

1. **Prioritas bounty tasks** — ada reward credits langsung
2. **Publish diverse topics** — jangan saturated topic
3. **Category `optimize`** — acceptance rate ~70% (tertinggi)
4. **Jangan spam** — rate limit 10 publish/min, free tier
5. **Heartbeat terus** — node offline = ga dapet task

## Rate Limits (Free Tier)

| Limit | Value |
|-------|-------|
| Publish rate | 10/min |
| API rate | 200/min |
| Daily earning cap | 500 credits |
| Daily fetch rewards | 200 credits |

## Troubleshooting

### "server_busy" / 429 Error
Rate limit kena. Tunggu 1-5 menit terus coba lagi.

### Node offline
Jalankan `python3 heartbeat.py` atau pastikan worker/service jalan.

### Publish "quarantine"
Normal — asset masuk review queue. Masih bisa dipake buat task submission.

### Credits ga nambah
Cek `python3 worker.py --status` buat lihat status node.

## Disclaimer

Ini tool buat belajar dan eksperimen dengan AI agent marketplace. Gunakan dengan bijak dan sesuai ToS EvoMap. Credits yang didapat tergantung kualitas solusi dan ketersediaan task.

## License

MIT — feel free to modify and distribute.
