# Waterloo CS Study Note Hub

A full-stack web application for sharing CS study notes, summaries, and guides in Markdown format using a Card-based UI.

## Quick Start

### One-Command Launch

```bash
python3 fix_and_start.py
```

That's it! The script automatically:
- Checks prerequisites (Python 3.8+, Node.js 18+)
- Creates virtual environment if needed
- Installs all dependencies (Backend and Frontend)
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
│   │   └── routes/           # API route modules
│   │       ├── topics.py     # Topic management
│   │       └── notes.py      # Study notes & comments
│   ├── frontend/             # React + TypeScript frontend
│   │   └── src/
│   │       ├── pages/        # Page components (Card View, Split View)
│   │       └── components/   # Reusable components
├── scripts/
│   └── seed_database.py      # Populate sample data
├── docs/
├── wcah.db                   # SQLite database file
├── fix_and_start.py          # Main launcher script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- SQLite - Lightweight database
- NoteType Enum - Categorize notes (Summary, Lecture, Code, Other)

**Frontend:**
- React 18 - UI library
- TypeScript - Type-safe JavaScript
- React Mde - Split-pane Markdown Editor
- Showdown - Markdown conversion
- Card UI - Modern layout for browsing notes

## Features

### For Students
- **Study Notes:** Create Markdown-rich notes with preview.
- **Card View:** Browse notes in a visual card layout with topic badges.
- **Navigation:** Deep link directly to notes with auto-generated Table of Contents.
- **Engagement:** Like notes and leave comments.
- **Categorization:** Tag notes as Summary, Lecture, Code, etc.

### For Professors
- Create and organize Courses and Topics.
- Users with 'Professor' role can manage all content.

## Manual Setup (Advanced)

If you prefer manual control over the setup process:

### Backend Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize database (first time only)
python scripts/seed_database.py

# Start backend server
uvicorn src.backend.main:app --reload
# Backend will run on http://localhost:8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd src/frontend

# Install npm dependencies
npm install

# Start development server
npm run dev
# Frontend will run on http://localhost:5173
```

## Database Management

### View Database Contents
```bash
python scripts/inspect_database.py
```

Interactive menu to view:
- All tables and row counts
- Users, courses, assignments
- Questions, solutions, comments

### Backup Database
```bash
# Create backup
python scripts/backup_database.py backup

# Restore from backup
python scripts/backup_database.py restore backup_YYYYMMDD_HHMMSS.db
```

### Reset Database
```bash
# Delete and recreate
rm wcah.db
python scripts/seed_database.py
```

### Direct SQL Access
```bash
sqlite3 wcah.db
# sqlite> .tables
# sqlite> SELECT * FROM users;
# sqlite> .quit
```

## Testing & Diagnostics

### Run Diagnostic Tests
```bash
python3 test_and_fix.py
```

This will test:
- Backend health and connectivity
- CORS configuration
- Authentication endpoints
- Database integrity
- Frontend server status

### Browser-Based Testing
Open `test-connection.html` in your browser for interactive testing.

### Complete Fix & Cleanup
If you encounter issues:
```bash
python3 fix_and_start.py
```

This script will:
- Stop all running servers
- Clean up processes and caches
- Reinstall dependencies
- Restart everything fresh

## Troubleshooting

### "Cannot connect to server" Error

**Cause:** Cached browser data (old tokens in localStorage)

**Solutions:**

1. **Open in incognito/private window** (easiest)

2. **Clear localStorage:**
   - Open DevTools (F12)
   - Console tab → Type: `localStorage.clear()`
   - Press Enter → Refresh page

3. **Complete fix:**
   ```bash
   python3 fix_and_start.py
   ```

### Port Already in Use

```bash
# Kill existing processes
pkill -f uvicorn  # Backend on port 8000
pkill -f vite     # Frontend on port 5173

# Or kill specific ports
fuser -k 8000/tcp
fuser -k 5173/tcp

# Then restart
python3 start.py
```

### Backend Not Starting

```bash
# Check logs
tail -f /tmp/wcah-backend.log

# Common issues:
# - Port 8000 in use → Kill process
# - Database locked → Close other connections
# - Missing dependencies → pip install -r requirements.txt
```

### Frontend Not Starting

```bash
# Check logs
tail -f /tmp/wcah-frontend.log

# Common issues:
# - Port 5173 in use → Kill process
# - Node modules issues → rm -rf node_modules && npm install
# - TypeScript errors → Check console output
```

### Database Issues

```bash
# Check if database exists
ls -lh wcah.db

# Check tables
sqlite3 wcah.db "SELECT name FROM sqlite_master WHERE type='table';"

# Reset if corrupted
rm wcah.db && python scripts/seed_database.py
```

## API Documentation

Start the backend and visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

**Authentication:**
```
POST /api/auth/signup      - Register new user
POST /api/auth/login       - Login and get JWT token
GET  /api/auth/me          - Get current user info
```

**Courses:**
```
GET  /api/courses/         - List all courses
POST /api/courses/         - Create course (professor only)
GET  /api/courses/{id}     - Get course details
POST /api/courses/{id}/enroll - Enroll in course
```

**Assignments:**
```
GET  /api/assignments/course/{id} - Get course assignments
POST /api/assignments/            - Create assignment (professor)
GET  /api/assignments/{id}        - Get assignment details
```

**Questions:**
```
GET  /api/questions/assignment/{id} - Get assignment questions
POST /api/questions/                - Create question (professor)
GET  /api/questions/{id}            - Get question with test cases
```

**Solutions:**
```
GET  /api/solutions/question/{id} - Get question solutions
POST /api/solutions/              - Submit solution
POST /api/solutions/{id}/like     - Like solution
GET  /api/solutions/{id}/comments - Get comments
POST /api/solutions/{id}/comments - Add comment
```

## Authentication

The application uses JWT (JSON Web Tokens):
- Tokens generated on login/signup
- Stored in browser localStorage
- Sent via `Authorization: Bearer <token>` header
- Protected routes require valid token

**Token Flow:**
1. User logs in → Backend generates JWT
2. Frontend stores token in localStorage
3. All API requests include token in headers
4. Backend validates token before processing

## Database Schema

### Core Models

**User**
- id, username, email, password_hash
- identity (student/professor)
- created_at

**Course**
- id, name, code, description
- professor_id → User
- created_at

**Assignment**
- id, title, description, due_date
- course_id → Course

**Question**
- id, title, description, difficulty
- starter_code, solution_code
- assignment_id → Assignment

**Solution**
- id, code, likes, is_public
- question_id → Question
- user_id → User

**Comment**
- id, content, created_at
- solution_id → Solution
- user_id → User

**Testcase**
- id, input, expected_output
- question_id → Question

See `docs/DATABASE.md` for complete schema details.

## Development Workflow

### Making Changes

1. **Backend changes:**
   - Edit files in `src/backend/`
   - Backend auto-reloads (uvicorn --reload)
   - Test at http://localhost:8000/docs

2. **Frontend changes:**
   - Edit files in `src/frontend/src/`
   - Vite hot-reloads instantly
   - Check browser console for errors

3. **Database changes:**
   - Update models in `src/backend/models.py`
   - Create migration: `alembic revision --autogenerate -m "description"`
   - Apply migration: `alembic upgrade head`

### Adding New Features

1. **Backend:**
   - Add model to `models.py`
   - Add schema to `schemas.py`
   - Create routes in `routes/`
   - Register router in `main.py`

2. **Frontend:**
   - Add types to `types.ts`
   - Add API methods to `api.ts`
   - Create page component in `pages/`
   - Add route to `App.tsx`

## Deployment

### Production Considerations

1. **Environment Variables:**
   - Move sensitive data to `.env` file
   - Use proper SECRET_KEY for JWT
   - Configure production database URL

2. **Backend:**
   - Use production ASGI server (Gunicorn + Uvicorn workers)
   - Enable HTTPS
   - Set appropriate CORS origins
   - Use PostgreSQL instead of SQLite

3. **Frontend:**
   - Build for production: `npm run build`
   - Serve static files with nginx/Apache
   - Update API_BASE_URL to production backend

4. **Database:**
   - Regular backups
   - Use connection pooling
   - Set up monitoring

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature-name`
6. Create pull request


## Team

Yi Xing

---

## Additional Documentation

- **QUICK_START.md** - Visual quick start guide
- **SOLUTION.md** - Detailed troubleshooting solutions
- **docs/DATABASE.md** - Complete database schema
- **docs/Charter.md** - Project charter and requirements

## Tips

- Always use incognito window when testing to avoid cache issues
- Check browser console (F12) for detailed error messages
- Use API docs at `/docs` for endpoint testing
- Run `python3 test_and_fix.py` if something breaks

**Questions?** Open an issue or check the documentation files.
