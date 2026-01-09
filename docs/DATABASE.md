# Database Documentation

## Overview
The Waterloo CS Study Note Hub uses SQLite as the database with SQLAlchemy ORM for data modeling and Alembic for migrations.

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
- One-to-many with `notes`
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
- One-to-many with `topics`

#### topics
- `id` (PK): Integer, auto-increment
- `title`: String(200)
- `description`: Text
- `course_id` (FK): Integer → courses.id
- `created_at`: DateTime

**Relationships:**
- Many-to-one with `courses`
- One-to-many with `notes`

#### study_notes
- `id` (PK): Integer, auto-increment
- `title`: String(200)
- `content`: Text (Markdown)
- `summary`: String(500)
- `resource_type`: Enum ('CheatSheet', 'Summary', 'Guide')
- `topic_id` (FK): Integer → topics.id
- `author_id` (FK): Integer → users.id
- `likes_count`: Integer
- `created_at`: DateTime

**Relationships:**
- Many-to-one with `topics`
- Many-to-one with `users` (author)
- One-to-many with `comments`
- Many-to-many with `users` (likes via user_note_likes)

#### comments
- `id` (PK): Integer, auto-increment
- `note_id` (FK): Integer → study_notes.id
- `user_id` (FK): Integer → users.id
- `content`: Text
- `created_at`: DateTime

#### user_courses (Association Table)
- `user_id` (FK): Integer
- `course_id` (FK): Integer

#### user_note_likes (Association Table)
- `user_id` (FK): Integer
- `note_id` (FK): Integer
