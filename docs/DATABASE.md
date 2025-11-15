# Database Documentation

## Overview
The Waterloo CS Assignment Hub uses SQLite as the database with SQLAlchemy ORM for data modeling and Alembic for migrations.

## Database Schema

### Tables

#### users
- `id` (PK): Integer, auto-increment
- `username`: String(50), unique, indexed
- `email`: String(100), unique
- `password_hash`: String(200)
- `identity`: String(20) - 'student' or 'professor'
- `created_at`: DateTime

**Relationships:**
- One-to-many with `courses` (as creator)
- Many-to-many with `courses` (as enrolled student)
- One-to-many with `solutions`
- One-to-many with `comments`

#### courses
- `id` (PK): Integer, auto-increment
- `course_code`: String(20), indexed
- `course_name`: String(200)
- `description`: Text
- `creator_id` (FK): Integer → users.id
- `created_at`: DateTime

**Relationships:**
- Many-to-one with `users` (creator)
- Many-to-many with `users` (enrolled students via user_courses)
- One-to-many with `assignments`

#### user_courses (Association Table)
- `user_id` (FK): Integer → users.id
- `course_id` (FK): Integer → courses.id
- Primary key: (user_id, course_id)

#### assignments
- `id` (PK): Integer, auto-increment
- `assignment_name`: String(200)
- `description`: Text
- `course_id` (FK): Integer → courses.id
- `created_at`: DateTime

**Relationships:**
- Many-to-one with `courses`
- One-to-many with `questions`

#### questions
- `id` (PK): Integer, auto-increment
- `title`: String(300), indexed
- `description`: Text
- `difficulty`: String(20) - 'easy', 'medium', or 'hard'
- `assignment_id` (FK): Integer → assignments.id
- `created_at`: DateTime

**Relationships:**
- Many-to-one with `assignments`
- One-to-many with `testcases`
- One-to-many with `solutions`

#### testcases
- `id` (PK): Integer, auto-increment
- `question_id` (FK): Integer → questions.id
- `input_data`: Text
- `expected_output`: Text
- `is_hidden`: Boolean (default: False)
- `created_at`: DateTime

**Relationships:**
- Many-to-one with `questions`

#### solutions
- `id` (PK): Integer, auto-increment
- `question_id` (FK): Integer → questions.id
- `submitter_id` (FK): Integer → users.id
- `code`: Text
- `language`: String(50)
- `status`: String(20) - 'pending', 'passed', 'failed'
- `likes`: Integer (default: 0)
- `submitted_at`: DateTime

**Relationships:**
- Many-to-one with `questions`
- Many-to-one with `users` (submitter)
- One-to-many with `comments`

#### comments
- `id` (PK): Integer, auto-increment
- `solution_id` (FK): Integer → solutions.id
- `user_id` (FK): Integer → users.id
- `content`: Text
- `created_at`: DateTime

**Relationships:**
- Many-to-one with `solutions`
- Many-to-one with `users`

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │
│ (Professor) │
└──────┬──────┘
       │ creates
       ↓
┌─────────────┐       ┌──────────────┐
│   Course    │───────│  Assignment  │
└──────┬──────┘       └──────┬───────┘
       │ enrolls            │ contains
       ↓                    ↓
┌─────────────┐       ┌──────────────┐       ┌───────────┐
│    User     │       │   Question   │───────│ Testcase  │
│  (Student)  │       └──────┬───────┘       └───────────┘
└──────┬──────┘              │ has
       │ submits             ↓
       ↓                ┌──────────────┐
┌─────────────┐        │   Solution   │
│   Comment   │────────│              │
└─────────────┘        └──────────────┘
```

## Migrations

Database migrations are managed using Alembic.

### Commands

**Create a new migration:**
```bash
source .venv/bin/activate
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations:**
```bash
alembic upgrade head
```

**Rollback one migration:**
```bash
alembic downgrade -1
```

**View migration history:**
```bash
alembic history
```

**Check current version:**
```bash
alembic current
```

## Database Management Scripts

### Seed Database
Populates the database with sample data for development/testing.

```bash
python scripts/seed_database.py
```

**Creates:**
- 5 users (2 professors, 3 students)
- 3 courses (CS137, CS138, CS246)
- 4 assignments
- 4 questions with testcases
- 4 sample solutions
- 4 comments

**All passwords:** `password123`

### Inspect Database
Interactive tool to view database contents and statistics.

```bash
python scripts/inspect_database.py
```

**Features:**
- Table row counts
- User listings
- Course enrollments
- Assignment summaries
- Question details
- Solution statistics
- Detailed views for specific tables

### Backup & Restore
Manage database backups.

```bash
python scripts/backup_database.py
```

**Features:**
- Create timestamped backups
- List all backups
- Restore from any backup
- Automatic backup before restore

## Database File Location

**File:** `wcah.db` (SQLite database)
**Location:** Project root directory

## Connection String

```python
sqlite:///./wcah.db
```

## Accessing the Database

### Via Python (SQLAlchemy)
```python
from src.backend.database import SessionLocal

db = SessionLocal()
try:
    # Query users
    users = db.query(User).all()
    
    # Create a course
    course = Course(
        course_code="CS137",
        course_name="Programming Principles",
        creator_id=1
    )
    db.add(course)
    db.commit()
finally:
    db.close()
```

### Via SQLite CLI
```bash
sqlite3 wcah.db

# View tables
.tables

# Query data
SELECT * FROM users;

# Exit
.quit
```

### Via Python DB-API
```python
import sqlite3

conn = sqlite3.connect('wcah.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

conn.close()
```

## Best Practices

1. **Always use migrations** for schema changes - never modify `wcah.db` directly
2. **Use the session dependency** `get_db()` in API endpoints for automatic session management
3. **Commit transactions explicitly** when using raw sessions
4. **Close sessions** in finally blocks to prevent connection leaks
5. **Create backups** before applying migrations in production
6. **Use seed script** to reset database during development

## Development Workflow

### Initial Setup
```bash
# Create database (happens automatically on first app startup)
python -c "from src.backend.database import init_db; init_db()"

# Or start the backend (which calls init_db)
cd src/backend && uvicorn main:app --reload
```

### Adding Sample Data
```bash
python scripts/seed_database.py
```

### Making Schema Changes
1. Modify models in `src/backend/models.py`
2. Create migration: `alembic revision --autogenerate -m "Add new column"`
3. Review the generated migration in `src/database/versions/`
4. Apply migration: `alembic upgrade head`

### Resetting Database
```bash
# Method 1: Delete and recreate
rm wcah.db
python scripts/seed_database.py

# Method 2: Restore from backup
python scripts/backup_database.py
# Choose option 3 (restore)
```

## Troubleshooting

### Migration conflicts
```bash
# View current state
alembic current
alembic history

# Rollback problematic migration
alembic downgrade -1

# Fix models and create new migration
alembic revision --autogenerate -m "Fix schema"
```

### Database locked
SQLite can only handle one write at a time. Ensure:
- Only one backend server is running
- Close all connections after use
- Use connection pooling settings

### Foreign key violations
Enable foreign key constraints (default in our setup):
```python
# In database.py
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)
```

## Production Considerations

For production deployment, consider:
1. **PostgreSQL/MySQL** for better concurrency and performance
2. **Connection pooling** settings tuned for your load
3. **Regular backups** automated via cron jobs
4. **Migration testing** in staging environment first
5. **Read replicas** for scaling read-heavy workloads

## File Structure

```
cs137-web-app/
├── wcah.db                        # SQLite database file
├── alembic.ini                    # Alembic configuration
├── src/
│   ├── backend/
│   │   ├── database.py            # Database connection & session
│   │   └── models.py              # SQLAlchemy models
│   └── database/
│       ├── env.py                 # Alembic environment config
│       ├── script.py.mako         # Migration template
│       └── versions/              # Migration files
│           └── xxx_initial_schema.py
├── scripts/
│   ├── seed_database.py           # Populate with sample data
│   ├── inspect_database.py        # View database contents
│   └── backup_database.py         # Backup & restore utility
└── backups/                       # Database backup files (created on first backup)
```
