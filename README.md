# Waterloo CS Study Note Hub

A full-stack web application for sharing CS study notes, summaries, and guides in Markdown format.

## Quick Start

### One-Command Launch

```bash
python3 fix_and_start.py
```

The script automatically:
- Checks prerequisites (Python 3.8+, Node.js 18+)
- Creates virtual environment if needed
- Installs all dependencies
- Sets up and seeds database
- Starts backend server (port 8000)
- Starts frontend server (port 5173)

**Access the app:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Sample Accounts:**
- Professor: `prof_smith` / `password123`
- Student: `alice` / `password123`

**Stop:** Press `Ctrl+C` or run `pkill -f uvicorn && pkill -f vite`

## Project Structure

```
cs137-web-app/
├── src/
│   ├── backend/              # FastAPI backend
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── models.py         # SQLAlchemy database models
│   │   ├── schemas.py        # Pydantic validation schemas
│   │   ├── auth.py           # JWT authentication
│   │   ├── database.py       # Database configuration
│   │   └── routes/           # API route modules
│   │       ├── auth.py       # Authentication endpoints
│   │       ├── courses.py    # Course management
│   │       ├── topics.py     # Topic management
│   │       └── notes.py      # Study notes & comments
│   ├── frontend/             # React + TypeScript frontend
│   │   └── src/
│   │       ├── api.ts        # Type-safe API client
│   │       ├── AuthContext.tsx  # Auth state management
│   │       ├── pages/        # Page components
│   │       └── components/   # Reusable components
│   └── database/             # Alembic migrations
├── scripts/
│   ├── seed_database.py      # Populate sample data
│   ├── inspect_database.py   # View database contents
│   └── backup_database.py    # Backup/restore utility
├── docs/
│   ├── Charter.md            # Project charter
│   └── DATABASE.md           # Database schema documentation
├── wcah.db                   # SQLite database file
├── fix_and_start.py          # Main launcher script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Tech Stack

**Backend:**
- FastAPI 0.104.1 - Modern, fast Python web framework
- SQLAlchemy 2.0.23 - SQL toolkit and ORM
- SQLite - Lightweight database
- Alembic 1.12.1 - Database migrations
- JWT + bcrypt - Secure authentication

**Frontend:**
- React 18.3.1 - UI library
- TypeScript 5.9.3 - Type-safe JavaScript
- Vite 4.5.14 - Lightning-fast build tool
- React Router 6.30.2 - Client-side routing
- React Markdown - Markdown rendering for notes

## Features

### For Students
- Browse and enroll in courses
- View topics within courses
- Create and share study notes (Cheat Sheets, Summaries, Guides)
- Write content in Markdown
- Like and comment on other students' notes
- Learn from peer resources

### For Professors
- Create and manage courses (admin privileges)
- Create course topics
- Monitor student activity
- Moderate content (delete any note/topic)
