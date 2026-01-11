# SE-StudyCenter

**SE-StudyCenter** is a full-stack web application for sharing CS study materials, notes, and summaries using a Card-based UI and Markdown editor.

## 🚀 Quick Start

**Get started in one step:**

```bash
python3 start.py
```

This script handles everything: environment setup, dependencies, database seeding, and server launch.

**Access the App:**
*   **Frontend:** [http://localhost:5173](http://localhost:5173)
*   **Backend API:** [http://localhost:8000/docs](http://localhost:8000/docs)

**Login Credentials:**
*   **Student:** `alice` / `password123`
*   **Professor:** `prof_smith` / `password123`

---

## ✨ Features

*   **Markdown Notes:** Create and preview rich text study notes.
*   **Card UI:** Organize content visually with topic badges.
*   **Engagement:** Like, comment, and share notes.
*   **Role-Based Access:** Professors manage courses/topics; students contribute content.

## 🛠️ Tech Stack

*   **Backend:** Python (FastAPI), SQLAlchemy, SQLite.
*   **Frontend:** React (TypeScript, Vite), React Mde.

## 💻 Developer Guide

### Manual Setup
If you prefer manual control:
1.  **Backend:** Create venv, install `requirements.txt`, run `uvicorn src.backend.main:app --reload`.
2.  **Frontend:** `cd src/frontend`, `npm install`, `npm run dev`.

### Troubleshooting
*   **Connection Failed?** Try an Incognito window or clear `localStorage`.
*   **Ports in Use?** Run `pkill -f uvicorn && pkill -f vite` to free ports 8000/5173.
*   **Reset Application?** Run `python3 start.py` again to clean and restart.

### Documentation
*   [Database Schema](docs/DATABASE.md)
*   [Project Charter](docs/Charter.md)
*   [Troubleshooting Details](SOLUTION.md)

## 👥 Team
Yi Xing
