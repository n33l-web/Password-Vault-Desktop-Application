import mysql.connector
from dotenv import load_dotenv
import os
from encryption import hash_master_password, verify_master_password

# --- Load environment variables from .env file ---
load_dotenv()

# --- Get credentials from environment ---
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# --- MySQL Connection ---
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)
cursor = db.cursor()

def insert_user(username, hashed_password):
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
        (username, hashed_password)
    )
    db.commit()


def get_user_by_username(username):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()

def set_security_questions(user_id, q1, a1, q2, a2, q3, a3):
    cursor.execute(
        "INSERT INTO security_questions (user_id, question1, answer1_hash, question2, answer2_hash, question3, answer3_hash) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (user_id, q1, hash_master_password(a1), q2, hash_master_password(a2), q3, hash_master_password(a3))
    )
    db.commit()

def get_questions_by_username(username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return None
    user_id = user[0]
    cursor.execute("SELECT question1, question2, question3 FROM security_questions WHERE user_id = %s", (user_id,))
    return cursor.fetchone(), user_id

def verify_security_answers(user_id, a1, a2, a3):
    cursor.execute("SELECT answer1_hash, answer2_hash, answer3_hash FROM security_questions WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if not result:
        return False
    return (verify_master_password(a1, result[0].encode()) and
            verify_master_password(a2, result[1].encode()) and
            verify_master_password(a3, result[2].encode()))
