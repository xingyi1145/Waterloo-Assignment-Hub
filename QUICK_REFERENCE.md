# Database Quick Reference

## 🚀 Common Commands

### Seed Database with Sample Data
```bash
cd /home/xingy/cs137-web-app
source .venv/bin/activate
python scripts/seed_database.py
```

### View Database Contents
```bash
python scripts/inspect_database.py
```

### Backup Database
```bash
python scripts/backup_database.py
```

### Create Migration (after modifying models)
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## 📊 Sample Credentials

All passwords: `password123`

**Professors:**
- `prof_smith` (smith@uwaterloo.ca) - Created CS137, CS138
- `prof_jones` (jones@uwaterloo.ca) - Created CS246

**Students:**
- `alice` (alice@uwaterloo.ca) - Enrolled in CS137, CS138
- `bob` (bob@uwaterloo.ca) - Enrolled in CS137, CS246
- `charlie` (charlie@uwaterloo.ca) - Enrolled in CS138

## 📁 Key Files

- `wcah.db` - SQLite database
- `alembic.ini` - Migration config
- `src/database/versions/` - Migration files
- `scripts/seed_database.py` - Sample data
- `scripts/inspect_database.py` - Database viewer
- `scripts/backup_database.py` - Backup utility
- `docs/DATABASE.md` - Full documentation

## 🔢 Current Data Counts

- Users: 5
- Courses: 3
- Assignments: 4
- Questions: 4
- Testcases: 14
- Solutions: 4
- Comments: 4
