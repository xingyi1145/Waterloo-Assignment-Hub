# Quick Start Guide

## Run the App in 3 Steps

### 1. Start Everything
```bash
python3 fix_and_start.py
```

### 2. Open Browser
Go to: **http://localhost:5173**

### 3. Login
- Username: `alice` or `prof_smith`
- Password: `password123`

That's it!

---

## If You See "Cannot connect to server"

### Quick Fix (30 seconds)

**Option A:** Open in incognito/private window

**Option B:** Clear browser cache
1. Press `F12` (open DevTools)
2. Console tab
3. Type: `localStorage.clear()`
4. Press Enter
5. Refresh page

---

## Stop the App

Press `Ctrl+C` in the terminal

Or run:
```bash
pkill -f uvicorn && pkill -f vite
```

---

## What You Get

- Backend API: http://localhost:8000
- Frontend App: http://localhost:5173  
- API Docs: http://localhost:8000/docs
- Sample database with users and courses

---

## Need More Help?

- Full docs: See `README.md`
- Troubleshooting: See `SOLUTION.md`
