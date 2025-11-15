"""
Database inspection utility
Shows statistics and contents of the database
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import func
from src.backend.database import SessionLocal, init_db
from src.backend.models import User, Course, Assignment, Question, Testcase, Solution, Comment


def print_table_stats(db):
    """Print statistics for all tables"""
    print("\n📊 Database Statistics")
    print("=" * 60)
    
    stats = [
        ("Users", db.query(User).count()),
        ("Courses", db.query(Course).count()),
        ("Assignments", db.query(Assignment).count()),
        ("Questions", db.query(Question).count()),
        ("Testcases", db.query(Testcase).count()),
        ("Solutions", db.query(Solution).count()),
        ("Comments", db.query(Comment).count()),
    ]
    
    for table_name, count in stats:
        print(f"  {table_name:.<20} {count:>5}")
    
    print("=" * 60)


def print_users(db):
    """Print all users"""
    print("\n👥 Users")
    print("-" * 60)
    users = db.query(User).all()
    for user in users:
        print(f"  [{user.id}] {user.username:.<20} {user.email:.<30} {user.identity}")


def print_courses(db):
    """Print all courses with enrollment counts"""
    print("\n📚 Courses")
    print("-" * 60)
    courses = db.query(Course).all()
    for course in courses:
        enrollment_count = len(course.enrolled_students)
        assignment_count = len(course.assignments)
        print(f"  [{course.id}] {course.course_code} - {course.course_name}")
        print(f"      Enrollments: {enrollment_count}, Assignments: {assignment_count}")


def print_assignments(db):
    """Print all assignments with question counts"""
    print("\n📝 Assignments")
    print("-" * 60)
    assignments = db.query(Assignment).all()
    for assignment in assignments:
        question_count = len(assignment.questions)
        course = db.query(Course).filter(Course.id == assignment.course_id).first()
        print(f"  [{assignment.id}] {assignment.assignment_name}")
        print(f"      Course: {course.course_code}, Questions: {question_count}")


def print_questions(db):
    """Print all questions with solution and testcase counts"""
    print("\n❓ Questions")
    print("-" * 60)
    questions = db.query(Question).all()
    for question in questions:
        solution_count = len(question.solutions)
        testcase_count = len(question.testcases)
        print(f"  [{question.id}] {question.title} ({question.difficulty})")
        print(f"      Solutions: {solution_count}, Testcases: {testcase_count}")


def print_solutions(db):
    """Print solution statistics"""
    print("\n💡 Solutions")
    print("-" * 60)
    solutions = db.query(Solution).all()
    for solution in solutions:
        user = db.query(User).filter(User.id == solution.submitter_id).first()
        question = db.query(Question).filter(Question.id == solution.question_id).first()
        comment_count = len(solution.comments)
        print(f"  [{solution.id}] {question.title[:40]}")
        print(f"      By: {user.username}, Status: {solution.status}, Likes: {solution.likes}, Comments: {comment_count}")


def print_detailed_view(db, table_name):
    """Print detailed view of a specific table"""
    if table_name == "users":
        users = db.query(User).all()
        for user in users:
            print(f"\n{'='*60}")
            print(f"User ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Identity: {user.identity}")
            print(f"Enrolled Courses: {len(user.enrolled_courses)}")
            print(f"Submitted Solutions: {len(user.solutions)}")
            if user.identity == "professor":
                print(f"Created Courses: {len(user.created_courses)}")
    
    elif table_name == "courses":
        courses = db.query(Course).all()
        for course in courses:
            creator = db.query(User).filter(User.id == course.creator_id).first()
            print(f"\n{'='*60}")
            print(f"Course ID: {course.id}")
            print(f"Code: {course.course_code}")
            print(f"Name: {course.course_name}")
            print(f"Description: {course.description}")
            print(f"Creator: {creator.username}")
            print(f"Enrollments: {len(course.enrolled_students)}")
            print(f"Assignments: {len(course.assignments)}")
    
    elif table_name == "solutions":
        solutions = db.query(Solution).all()
        for solution in solutions:
            user = db.query(User).filter(User.id == solution.submitter_id).first()
            question = db.query(Question).filter(Question.id == solution.question_id).first()
            print(f"\n{'='*60}")
            print(f"Solution ID: {solution.id}")
            print(f"Question: {question.title}")
            print(f"Submitter: {user.username}")
            print(f"Language: {solution.language}")
            print(f"Status: {solution.status}")
            print(f"Likes: {solution.likes}")
            print(f"Comments: {len(solution.comments)}")
            print(f"\nCode:\n{solution.code}")


def main():
    """Main inspection function"""
    print("\n🔍 Database Inspector")
    print("=" * 60)
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Print overall statistics
        print_table_stats(db)
        
        # Print summaries
        print_users(db)
        print_courses(db)
        print_assignments(db)
        print_questions(db)
        print_solutions(db)
        
        # Interactive mode
        print("\n" + "=" * 60)
        print("💡 Detailed View Available")
        print("  Options: users, courses, solutions, or 'exit'")
        
        while True:
            choice = input("\nEnter table name for details (or 'exit'): ").strip().lower()
            if choice == 'exit':
                break
            elif choice in ['users', 'courses', 'solutions']:
                print_detailed_view(db, choice)
            else:
                print("❌ Invalid option. Try: users, courses, solutions, or exit")
        
        print("\n✅ Inspection complete\n")
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
