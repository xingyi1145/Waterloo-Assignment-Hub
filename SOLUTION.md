# Troubleshooting Guide

## "Cannot connect to server" Error

### Root Cause
Your servers are running fine. The error is from **cached browser data** (old expired token in localStorage).

### Solutions

#### Solution 1: Incognito Window (Easiest)
Open http://localhost:5173 in an **incognito/private window**

#### Solution 2: Clear localStorage
1. Open the app in browser
2. Press `F12` (DevTools)
3. Go to **Console** tab
4. Type: `localStorage.clear()`
5. Press Enter
6. Refresh page (`Ctrl+Shift+R`)

#### Solution 3: Complete Fix
```bash
python3 fix_and_start.py
```
Then open in incognito window

---

## Port Already in Use

### Problem
`Address already in use: 8000` or `5173`

### Solution
```bash
# Kill existing servers
pkill -f uvicorn  # Backend
pkill -f vite     # Frontend

# Or kill specific ports
fuser -k 8000/tcp
fuser -k 5173/tcp

# Restart
python3 start.py
```

---

## Backend Not Starting

### Check if running
```bash
curl http://localhost:8000/api/health
```

### View logs
```bash
tail -f /tmp/wcah-backend.log
```

### Common fixes
```bash
# Reinstall dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Check database
ls -lh wcah.db

# Reset database if needed
rm wcah.db
python scripts/seed_database.py
```

---

## Frontend Not Starting

### Check if running
```bash
curl http://localhost:5173
```

### View logs
```bash
tail -f /tmp/wcah-frontend.log
```

### Common fixes
```bash
cd src/frontend

# Clear node_modules
rm -rf node_modules
npm install

# Clear Vite cache
rm -rf node_modules/.vite
```

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
