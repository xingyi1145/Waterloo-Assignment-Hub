# Quick Start Guide

## Run the App in 3 Steps

### 1. Start Everything
```bash
python3 fix_and_start.py
```
*Note: This script handles dependencies, database seeding, and server startup automatically.*

### 2. Open Browser
Go to: **http://localhost:5173**

### 3. Login
- **Student:** `alice` / `password123`
- **Professor:** `prof_smith` / `password123`

That's it!

---

## Troubleshooting

### "Cannot connect to server"
Typically a browser cache issue.
1. Open in **Incognito/Private** window.
2. Or clear cache manually: `F12` -> Console -> type `localStorage.clear()` -> Refresh.

### Database Issues
If login fails ("User not found"), run:
```bash
python scripts/seed_database.py
```
(Ensure you are in the virtual environment or use `.venv/bin/python`).

---

## Stop the App

Press `Ctrl+C` in the terminal

Or run:
```bash
pkill -f uvicorn && pkill -f vite
```

