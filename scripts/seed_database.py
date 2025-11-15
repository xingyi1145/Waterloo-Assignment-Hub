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
from src.backend.models import User, Course, Assignment, Question, Testcase, Solution, Comment
from src.backend.auth import get_password_hash


def clear_database(db: Session):
    """Clear all data from database"""
    print("🗑️  Clearing existing data...")
    db.query(Comment).delete()
    db.query(Solution).delete()
    db.query(Testcase).delete()
    db.query(Question).delete()
    db.query(Assignment).delete()
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
    
    # Enroll students in courses
    users["alice"].enrolled_courses.extend([courses[0], courses[1]])
    users["bob"].enrolled_courses.extend([courses[0], courses[2]])
    users["charlie"].enrolled_courses.append(courses[1])
    db.commit()
    
    print(f"✅ Created {len(courses)} courses")
    return courses


def seed_assignments(db: Session, courses: list):
    """Create sample assignments"""
    print("📝 Creating assignments...")
    
    assignments = [
        # CS137 Assignments
        Assignment(
            assignment_name="Assignment 1: Python Basics",
            description="Introduction to Python programming fundamentals",
            course_id=courses[0].id
        ),
        Assignment(
            assignment_name="Assignment 2: Control Flow",
            description="Practice with conditionals, loops, and functions",
            course_id=courses[0].id
        ),
        # CS138 Assignments
        Assignment(
            assignment_name="Assignment 1: Arrays and Lists",
            description="Working with linear data structures",
            course_id=courses[1].id
        ),
        # CS246 Assignment
        Assignment(
            assignment_name="Assignment 1: C++ Basics",
            description="Introduction to C++ syntax and compilation",
            course_id=courses[2].id
        ),
    ]
    
    for assignment in assignments:
        db.add(assignment)
    db.commit()
    
    print(f"✅ Created {len(assignments)} assignments")
    return assignments


def seed_questions(db: Session, assignments: list):
    """Create sample questions with testcases"""
    print("❓ Creating questions...")
    
    # CS137 Assignment 1 Questions
    q1 = Question(
        title="Sum of Two Numbers",
        description="""Write a function that takes two integers as input and returns their sum.

Function signature:
def add_numbers(a: int, b: int) -> int:
    pass

Examples:
- add_numbers(5, 3) should return 8
- add_numbers(-1, 1) should return 0
- add_numbers(0, 0) should return 0""",
        difficulty="easy",
        assignment_id=assignments[0].id
    )
    db.add(q1)
    db.commit()
    
    # Add testcases for q1
    testcases_q1 = [
        Testcase(question_id=q1.id, input_data="5, 3", expected_output="8", is_hidden=False),
        Testcase(question_id=q1.id, input_data="-1, 1", expected_output="0", is_hidden=False),
        Testcase(question_id=q1.id, input_data="0, 0", expected_output="0", is_hidden=False),
        Testcase(question_id=q1.id, input_data="100, 200", expected_output="300", is_hidden=True),
    ]
    for tc in testcases_q1:
        db.add(tc)
    
    q2 = Question(
        title="Reverse a String",
        description="""Write a function that reverses a string.

Function signature:
def reverse_string(s: str) -> str:
    pass

Examples:
- reverse_string("hello") should return "olleh"
- reverse_string("Python") should return "nohtyP"
- reverse_string("") should return ""
- reverse_string("a") should return "a" """,
        difficulty="easy",
        assignment_id=assignments[0].id
    )
    db.add(q2)
    db.commit()
    
    testcases_q2 = [
        Testcase(question_id=q2.id, input_data="hello", expected_output="olleh", is_hidden=False),
        Testcase(question_id=q2.id, input_data="Python", expected_output="nohtyP", is_hidden=False),
        Testcase(question_id=q2.id, input_data="", expected_output="", is_hidden=True),
    ]
    for tc in testcases_q2:
        db.add(tc)
    
    # CS137 Assignment 2 Question
    q3 = Question(
        title="Fibonacci Sequence",
        description="""Write a function that returns the nth Fibonacci number.

The Fibonacci sequence starts: 0, 1, 1, 2, 3, 5, 8, 13, 21...

Function signature:
def fibonacci(n: int) -> int:
    pass

Examples:
- fibonacci(0) should return 0
- fibonacci(1) should return 1
- fibonacci(6) should return 8
- fibonacci(10) should return 55""",
        difficulty="medium",
        assignment_id=assignments[1].id
    )
    db.add(q3)
    db.commit()
    
    testcases_q3 = [
        Testcase(question_id=q3.id, input_data="0", expected_output="0", is_hidden=False),
        Testcase(question_id=q3.id, input_data="1", expected_output="1", is_hidden=False),
        Testcase(question_id=q3.id, input_data="6", expected_output="8", is_hidden=False),
        Testcase(question_id=q3.id, input_data="10", expected_output="55", is_hidden=True),
    ]
    for tc in testcases_q3:
        db.add(tc)
    
    # CS138 Question
    q4 = Question(
        title="Find Maximum in Array",
        description="""Write a function that finds the maximum value in an array of integers.

Function signature:
def find_max(arr: list[int]) -> int:
    pass

You can assume the array is non-empty.

Examples:
- find_max([1, 5, 3, 9, 2]) should return 9
- find_max([10]) should return 10
- find_max([-5, -1, -10, -3]) should return -1""",
        difficulty="easy",
        assignment_id=assignments[2].id
    )
    db.add(q4)
    db.commit()
    
    testcases_q4 = [
        Testcase(question_id=q4.id, input_data="[1, 5, 3, 9, 2]", expected_output="9", is_hidden=False),
        Testcase(question_id=q4.id, input_data="[10]", expected_output="10", is_hidden=False),
        Testcase(question_id=q4.id, input_data="[-5, -1, -10, -3]", expected_output="-1", is_hidden=True),
    ]
    for tc in testcases_q4:
        db.add(tc)
    
    db.commit()
    print(f"✅ Created 4 questions with testcases")
    return [q1, q2, q3, q4]


def seed_solutions(db: Session, questions: list, users: dict):
    """Create sample solutions"""
    print("💡 Creating solutions...")
    
    solutions = [
        # Alice's solution to Sum of Two Numbers
        Solution(
            question_id=questions[0].id,
            submitter_id=users["alice"].id,
            code="""def add_numbers(a: int, b: int) -> int:
    return a + b""",
            language="python",
            status="passed",
            likes=5
        ),
        # Bob's solution to Sum of Two Numbers
        Solution(
            question_id=questions[0].id,
            submitter_id=users["bob"].id,
            code="""def add_numbers(a: int, b: int) -> int:
    # Using explicit sum
    result = a + b
    return result""",
            language="python",
            status="passed",
            likes=2
        ),
        # Alice's solution to Reverse String
        Solution(
            question_id=questions[1].id,
            submitter_id=users["alice"].id,
            code="""def reverse_string(s: str) -> str:
    return s[::-1]""",
            language="python",
            status="passed",
            likes=8
        ),
        # Charlie's solution to Reverse String
        Solution(
            question_id=questions[1].id,
            submitter_id=users["charlie"].id,
            code="""def reverse_string(s: str) -> str:
    # Using a loop
    result = ""
    for char in s:
        result = char + result
    return result""",
            language="python",
            status="passed",
            likes=3
        ),
    ]
    
    for solution in solutions:
        db.add(solution)
    db.commit()
    
    print(f"✅ Created {len(solutions)} solutions")
    return solutions


def seed_comments(db: Session, solutions: list, users: dict):
    """Create sample comments"""
    print("💬 Creating comments...")
    
    comments = [
        Comment(
            solution_id=solutions[0].id,
            user_id=users["bob"].id,
            content="Clean and simple solution! 👍"
        ),
        Comment(
            solution_id=solutions[0].id,
            user_id=users["charlie"].id,
            content="Perfect example of writing Pythonic code."
        ),
        Comment(
            solution_id=solutions[2].id,
            user_id=users["bob"].id,
            content="Nice use of slicing! Very elegant."
        ),
        Comment(
            solution_id=solutions[3].id,
            user_id=users["alice"].id,
            content="Good approach using a loop. Shows clear understanding of the algorithm."
        ),
    ]
    
    for comment in comments:
        db.add(comment)
    db.commit()
    
    print(f"✅ Created {len(comments)} comments")


def main():
    """Main function to seed the database"""
    print("\n🌱 Database Seeding Script")
    print("=" * 50)
    
    # Initialize database
    print("📊 Initializing database...")
    init_db()
    print("✅ Database initialized")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Ask for confirmation
        response = input("\n⚠️  This will clear all existing data. Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Seeding cancelled")
            return
        
        # Clear existing data
        clear_database(db)
        
        # Seed data
        users = seed_users(db)
        courses = seed_courses(db, users)
        assignments = seed_assignments(db, courses)
        questions = seed_questions(db, assignments)
        solutions = seed_solutions(db, questions, users)
        seed_comments(db, solutions, users)
        
        print("\n" + "=" * 50)
        print("✨ Database seeding complete!")
        print("\n📊 Summary:")
        print(f"  • Users: {len(users)}")
        print(f"  • Courses: {len(courses)}")
        print(f"  • Assignments: {len(assignments)}")
        print(f"  • Questions: 4 (with testcases)")
        print(f"  • Solutions: {len(solutions)}")
        print(f"  • Comments: 4")
        print("\n🔑 Login credentials (all passwords: 'password123'):")
        print("  Professors: prof_smith, prof_jones")
        print("  Students: alice, bob, charlie")
        print("=" * 50 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
