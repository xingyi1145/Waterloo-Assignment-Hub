# Troubleshooting Guide

## "Cannot connect to server" Error

### Root Cause
Typically caused by cached browser data (old tokens) or servers not running, especially after database resets.

### Solutions

#### Solution 1: Complete Fix (Recommended)
This script re-installs dependencies and restarts everything freshly.
```bash
python3 fix_and_start.py
```
After running, open http://localhost:5173 (preferably in Incognito/Private mode).

#### Solution 2: Clear localStorage
1. Open DevTools (`F12`)
2. Console tab -> Type `localStorage.clear()` -> Enter
3. Refresh page

---

## Port Already in Use

### Problem
`Address already in use: 8000` or `5173`

### Solution
```bash
# Kill existing servers
pkill -f uvicorn
pkill -f vite
```
Then run `python3 fix_and_start.py` again.

---

## Login Issues

### "User not found" or "Incorrect password"
If you reset the database manually, the default users might be missing.

**Fix:** Run the seeder manually (if `fix_and_start.py` didn't catch it):
```bash
source .venv/bin/activate  # or .venv/Scripts/activate on Windows
python scripts/seed_database.py
```
This restores users: `alice` (student) and `prof_smith` (professor).

---

## Backend Not Starting

### Check Logs
```bash
tail -f /tmp/wcah-backend.log
```

### Common Issues
- **Missing Database:** Run `python scripts/seed_database.py`
- **Dependency Mismatch:** Run `pip install -r requirements.txt` (specifically check `bcrypt` version).

---

## Frontend Not Starting

### Common Issues
- **Legacy Peer Deps:** If `npm install` fails, run `npm install --legacy-peer-deps` (handled automatically by `fix_and_start.py`).


---

## TypeScript Errors

### Missing @types/node
```bash
cd src/frontend
npm install --save-dev @types/node
```

---

## Database Issues

### View database
```bash
python scripts/inspect_database.py
```

### Check tables
```bash
sqlite3 wcah.db ".tables"
```

### Reset database
```bash
rm wcah.db
python scripts/seed_database.py
```

### Backup before reset
```bash
python scripts/backup_database.py backup
```

---

## Still Having Issues?

### 1. Check logs
```bash
# Backend logs
tail -f /tmp/wcah-backend.log

# Frontend logs  
tail -f /tmp/wcah-frontend.log
```

### 2. Check processes
```bash
ps aux | grep -E "uvicorn|vite"
```

### 3. Check ports
```bash
lsof -i :8000  # Backend
lsof -i :5173  # Frontend
```

### 4. Complete cleanup
```bash
# Stop everything
pkill -f uvicorn && pkill -f vite

# Clean up
rm -rf src/frontend/node_modules/.vite
rm -rf src/frontend/dist

# Restart fresh
python3 fix_and_start.py
```

---

## Quick Reference

### Start app
```bash
python3 fix_and_start.py
```

### Stop app
```bash
# Ctrl+C in terminal
# OR
pkill -f uvicorn && pkill -f vite
```

### Access URLs
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Sample accounts
- Professor: `prof_smith` / `password123`
- Student: `alice` / `password123`

---
