"""
Database initialization and seed data script
Run this to populate the database with sample data
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from src.backend.database import SessionLocal, init_db
from src.backend.models import User, Course, Topic, StudyNote, Comment, NoteType
from src.backend.auth import get_password_hash


def clear_database(db: Session):
    """Clear all data from database"""
    print("🗑️  Clearing existing data...")
    db.query(Comment).delete()
    db.query(StudyNote).delete()
    db.query(Topic).delete()
    db.query(Course).delete()
    db.query(User).delete()
    db.commit()
    print("✅ Database cleared")


def seed_users(db: Session):
    """Create sample users"""
    print("👥 Creating users...")
    
    users = [
        User(
            username="prof_smith",
            email="smith@uwaterloo.ca",
            password_hash=get_password_hash("password123"),
            identity="professor"
        ),
        User(
            username="prof_jones",
            email="jones@uwaterloo.ca",
            password_hash=get_password_hash("password123"),
            identity="professor"
        ),
        User(
            username="alice",
            email="alice@uwaterloo.ca",
            password_hash=get_password_hash("password123"),
            identity="student"
        ),
        User(
            username="bob",
            email="bob@uwaterloo.ca",
            password_hash=get_password_hash("password123"),
            identity="student"
        ),
        User(
            username="charlie",
            email="charlie@uwaterloo.ca",
            password_hash=get_password_hash("password123"),
            identity="student"
        ),
    ]
    
    for user in users:
        db.add(user)
    db.commit()
    
    print(f"✅ Created {len(users)} users")
    return {user.username: user for user in users}


def seed_courses(db: Session, users: dict):
    """Create sample courses"""
    print("📚 Creating courses...")
    
    courses = [
        Course(
            course_code="CS137",
            course_name="Programming Principles",
            description="Introduction to programming using Python and C. Fundamental programming concepts, data structures, and algorithms.",
            creator_id=users["prof_smith"].id
        ),
        Course(
            course_code="CS138",
            course_name="Introduction to Data Abstraction and Implementation",
            description="Introduction to data structures and their implementation. Topics include lists, stacks, queues, trees, and graphs.",
            creator_id=users["prof_smith"].id
        ),
        Course(
            course_code="CS246",
            course_name="Object-Oriented Software Development",
            description="Introduction to object-oriented programming and software development in C++. Design patterns and best practices.",
            creator_id=users["prof_jones"].id
        ),
    ]
    
    for course in courses:
        db.add(course)
    db.commit()
    
    print(f"✅ Created {len(courses)} courses")
    
    # Enroll students
    courses[0].enrolled_students.append(users["alice"])
    courses[0].enrolled_students.append(users["bob"])
    courses[1].enrolled_students.append(users["alice"])
    courses[2].enrolled_students.append(users["charlie"])
    db.commit()
    
    return {c.course_code: c for c in courses}


def seed_content(db: Session, courses: dict, users: dict):
    """Create topics and notes"""
    print("📝 Creating content...")
    
    # Topics for CS137
    cs137 = courses["CS137"]
    topics = [
        Topic(
            title="Pointers and Memory Management",
            description="Understanding stack vs heap, malloc/free, and pointer arithmetic.",
            course_id=cs137.id
        ),
        Topic(
            title="Recursion",
            description="Base cases, recursive steps, and tail recursion optimization.",
            course_id=cs137.id
        )
    ]
    
    for topic in topics:
        db.add(topic)
    db.commit()
    
    # Notes for Pointers
    pointers_topic = topics[0]
    notes = [
        StudyNote(
            title="Pointer Cheat Sheet",
            content="# Pointer Basics\n\n* `&x` : Address of x\n* `*p` : Value at address p\n\n## Malloc\n`int *arr = malloc(10 * sizeof(int));`",
            summary="Quick reference for pointer syntax",
            note_type=NoteType.Summary,
            topic_id=pointers_topic.id,
            author_id=users["alice"].id,
            likes=5
        ),
        StudyNote(
            title="Guide to Memory Leaks",
            content="# Avoiding Leaks\n\nAlways match `malloc` with `free`.\n\n```c\nint *p = malloc(sizeof(int));\nfree(p);\n```",
            summary="Best practices for memory management",
            note_type=NoteType.Code,
            topic_id=pointers_topic.id,
            author_id=users["prof_smith"].id,
            likes=12
        )
    ]
    
    for note in notes:
        db.add(note)
    db.commit()
    
    print(f"✅ Created {len(topics)} topics and {len(notes)} notes")


def main():
    """Main seed function"""
    init_db()
    db = SessionLocal()
    
    try:
        clear_database(db)
        users = seed_users(db)
        courses = seed_courses(db, users)
        seed_content(db, courses, users)
        print("\n✨ Database seeding completed successfully!")
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
