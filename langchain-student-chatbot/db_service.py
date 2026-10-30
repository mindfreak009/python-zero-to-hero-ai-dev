import sqlite3
from pathlib import Path

# Database file location
DB_PATH = Path("data/student_chatbot.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


# ================================================
# INITIALIZE DATABASE AND INSERT SAMPLE COURSES
# ================================================

def initialize_database():
    courses = [
        (
            "CS101", "Python Programming",
            "Learn Python fundamentals, functions, OOP, and file handling.",
            "3 Months", 5000.00, "12th Pass", "Online"
        ),
            (
                "CS102", "Web Development",
                "Learn HTML, CSS, JavaScript, and responsive web design.",
                "6 Months", 12000.00, "12th Pass", "Offline"
            ),
        (
            "CS103", "Data Science",
            "Learn Python, statistics, data analysis, and visualization.",
            "6 Months", 18000.00, "Graduate", "Online"
        ),
        (
            "CS104", "Machine Learning",
            "Understand machine learning algorithms and model development.",
            "4 Months", 15000.00,
            "Graduate in CS/IT or equivalent", "Hybrid"
        ),
        (
            "CS105", "Database Management",
            "Learn SQL, SQLite, database design, and normalization.",
            "2 Months", 4000.00, "12th Pass", "Online"
        ),
        (
            "CS106", "Java Programming",
            "Learn Java fundamentals, OOP, collections, and exceptions.",
            "4 Months", 9000.00, "12th Pass", "Offline"
        ),
        (
            "CS107", "Cyber Security",
            "Learn network security and ethical hacking fundamentals.",
            "5 Months", 16000.00, "12th Pass", "Hybrid"
        ),
    ]

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                description TEXT,
                duration TEXT,
                fee REAL,
                eligibility TEXT,
                mode TEXT
            )
        """)

        cursor.executemany("""
            INSERT OR IGNORE INTO courses (
                course_code,
                course_name,
                description,
                duration,
                fee,
                eligibility,
                mode
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, courses)

        connection.commit()
        print(f"Database initialized: {DB_PATH}")

    finally:
        connection.close()


# ================================================
# GET ALL COURSES
# ================================================

def get_all_courses():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM courses
            ORDER BY course_name
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# ================================================
# SEARCH COURSES
# ================================================

def search_course(keyword):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        search_term = f"%{keyword}%"

        cursor.execute("""
            SELECT *
            FROM courses
            WHERE course_code LIKE ?
               OR course_name LIKE ?
               OR description LIKE ?
               OR eligibility LIKE ?
               OR mode LIKE ?
            ORDER BY course_name
        """, (search_term,) * 5)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# ================================================
# GET COURSE BY CODE
# ================================================

def get_course_by_code(course_code):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM courses
            WHERE course_code = ?
        """, (course_code,))

        row = cursor.fetchone()
        return dict(row) if row else None

    finally:
        connection.close()


# ================================================
# DATABASE DIAGNOSTICS
# ================================================

def check_database():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """)

        tables = [row["name"] for row in cursor.fetchall()]

        print(f"Database path: {DB_PATH}")
        print(f"Tables: {tables}")
        print(f"Courses: {len(get_all_courses())}")

    finally:
        connection.close()


# ================================================
# RUN DIRECTLY
# ================================================

if __name__ == "__main__":
    initialize_database()
    check_database()