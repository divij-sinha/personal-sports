# Personal sports tracker

Tracks games over the next few weeks, shows previous results. **NOT UPDATED LIVE**.

## Teams to track

### Cricket

- India
- Kolkata Knight Riders
- Royal Challengers Bengaluru

### Football

- India
- Bengaluru FC
- ISL
- Chelsea FC
- Premier League
- Champions League

### American Football

- Chicago Bears

### Formula 1

- ALL

## Architecture 

┌───────────────────────────────────────────────┐
│          Personal / Intermittent Server       │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │ Cron Scheduler                           │  │
│  │ (runs when machine is on)                │  │
│  └───────────────┬─────────────────────────┘  │
│                  │                            │
│                  v                            │
│  ┌─────────────────────────────────────────┐  │
│  │ Python Snapshot Job                      │  │
│  │                                         │  │
│  │ 1. Fetch sports APIs                    │  │
│  │ 2. Normalize data                       │  │
│  │ 3. Compute status (upcoming/live/final) │  │
│  │ 4. Add generated_at timestamp           │  │
│  └───────────────┬─────────────────────────┘  │
│                  │ HTTPS (outbound only)       │
└──────────────────┼────────────────────────────┘
                   │
                   v
┌───────────────────────────────────────────────┐
│        Google Cloud Storage (Always-On)        │
│                                               │
│  Public Read Objects                           │
│                                               │
│  ├── today.json                               │
│  ├── upcoming.json                            │
│  ├── recent.json                              │
│  ├── index.html   (optional PWA hosting)      │
│  ├── app.js                                   │
│  └── sw.js        (service worker)             │
│                                               │
│  (Static hosting, no compute, no backend)      │
└──────────────────┬────────────────────────────┘
                   │ HTTPS GET
                   │
                   v
┌───────────────────────────────────────────────┐
│                User Devices                   │
│                                               │
│  iPhone / iPad / MacBook                      │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │ PWA (Installed or Browser)               │  │
│  │                                         │  │
│  │ - Fetch JSON snapshots                  │  │
│  │ - Render schedule + status              │  │
│  │ - Show "Updated X min ago"               │  │
│  │ - Cache via service worker               │  │
│  └─────────────────────────────────────────┘  │
│                                               │
│  (Works even if server is offline)             │
└───────────────────────────────────────────────┘
