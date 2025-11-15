# Waterloo CS Assignment Hub (WCAH)

A web platform for students to explore, solve, and share solutions to assignment-style programming problems from University of Waterloo CS courses. Professors can publish courses, assignments, and questions, while students can submit solutions and engage with peers through likes and comments.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+ and npm
- Git

### Backend Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd cs137-web-app
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database** (optional - happens automatically on first run):
   ```bash
   python scripts/seed_database.py
   ```
   This will create sample data (users, courses, assignments, questions).
   
   Default credentials (password: `password123`):
   - Professors: `prof_smith`, `prof_jones`
   - Students: `alice`, `bob`, `charlie`

5. **Run the FastAPI server**:
   ```bash
   uvicorn src.backend.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

5. **Access API documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd src/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

4. **Open in browser**:
   - Navigate to `http://localhost:5173`
   - Sign up as a student or professor
   - Start exploring!

## 📁 Project Structure

```
cs137-web-app/
├── docs/
│   ├── Charter.md              # Project charter and requirements
│   └── DATABASE.md             # Database schema and management guide
├── src/
│   ├── backend/
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── models.py          # SQLAlchemy database models
│   │   ├── schemas.py         # Pydantic validation schemas
│   │   ├── database.py        # Database configuration
│   │   ├── auth.py            # Authentication utilities (JWT, password hashing)
│   │   └── routes/            # API route handlers
│   │       ├── auth.py        # Authentication endpoints
│   │       ├── courses.py     # Course management
│   │       ├── assignments.py # Assignment management
│   │       ├── questions.py   # Question management
│   │       └── solutions.py   # Solution submission & comments
│   ├── database/              # Alembic migrations
│   │   ├── env.py             # Migration environment config
│   │   └── versions/          # Migration files
│   └── frontend/              # React + TypeScript frontend
│       ├── src/
│       │   ├── api.ts         # API client
│       │   ├── types.ts       # TypeScript types
│       │   ├── AuthContext.tsx # Auth state management
│       │   ├── pages/         # Page components
│       │   └── components/    # Reusable components
│       ├── package.json
│       └── vite.config.ts
├── scripts/
│   ├── seed_database.py       # Populate database with sample data
│   ├── inspect_database.py    # View database contents
│   └── backup_database.py     # Backup & restore utility
├── wcah.db                    # SQLite database file
├── alembic.ini                # Alembic configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user (student or professor)
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user information

### Courses
- `POST /api/courses/` - Create a new course (professors only)
- `GET /api/courses/` - List all courses
- `GET /api/courses/{course_id}` - Get course details
- `POST /api/courses/{course_id}/enroll` - Enroll in a course

### Assignments
- `POST /api/assignments/` - Create assignment (professors only)
- `GET /api/assignments/course/{course_id}` - List assignments for a course
- `GET /api/assignments/{assignment_id}` - Get assignment details

### Questions
- `POST /api/questions/` - Create question (professors only)
- `GET /api/questions/assignment/{assignment_id}` - List questions in an assignment
- `GET /api/questions/{question_id}` - Get question details

### Solutions
- `POST /api/solutions/` - Submit a solution
- `GET /api/solutions/question/{question_id}` - List solutions for a question
- `GET /api/solutions/{solution_id}` - Get solution details
- `POST /api/solutions/{solution_id}/like` - Like a solution
- `POST /api/solutions/{solution_id}/comments` - Add a comment
- `GET /api/solutions/{solution_id}/comments` - List comments

## 🧪 Testing the API

### Example: Register a Professor
```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "prof_smith",
    "email": "smith@uwaterloo.ca",
    "password": "securepass123",
    "identity": "professor"
  }'
```

### Example: Create a Course
```bash
curl -X POST "http://localhost:8000/api/courses/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "course_code": "CS137",
    "course_name": "Programming Principles",
    "description": "Introduction to programming in Python and C"
  }'
```

## 🗄️ Database

The application uses SQLite for development (stored as `wcah.db` in the project root). The database is automatically created when you first run the server.

### Database Schema

See [docs/DATABASE.md](docs/DATABASE.md) for detailed schema documentation.

**Main tables:**
- **Users**: username, email, password_hash, identity (student/professor)
- **Courses**: course_code, course_name, description, creator
- **Assignments**: assignment_name, description, course
- **Questions**: title, description, difficulty, assignment
- **Solutions**: code, language, status, likes, submitter
- **Comments**: content, solution, user
- **Testcases**: input_data, expected_output, question

### Database Management

**Seed with sample data:**
```bash
python scripts/seed_database.py
```

**Inspect database:**
```bash
python scripts/inspect_database.py
```

**Backup/restore:**
```bash
python scripts/backup_database.py
```

## 🛠️ Development

### Running in Development Mode
```bash
uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations
```bash
# Create a migration after modifying models
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## 🔒 Security Notes

⚠️ **Important**: The current implementation uses a hardcoded `SECRET_KEY` in `src/backend/auth.py`. 

**Before deploying to production:**
1. Generate a secure random key: `openssl rand -hex 32`
2. Store it in an environment variable
3. Update `auth.py` to read from `os.getenv("SECRET_KEY")`

## 📋 TODO / Roadmap

- [ ] Implement testcase execution sandbox
- [ ] Add frontend (React + TypeScript)
- [ ] Add solution ranking algorithm
- [ ] Implement badge/achievement system
- [ ] Add code syntax highlighting
- [ ] Email verification for signups
- [ ] Password reset functionality
- [ ] Admin dashboard
- [ ] Deployment guide (Docker, Railway, etc.)

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

See `docs/Charter.md` for project goals and architecture decisions.
