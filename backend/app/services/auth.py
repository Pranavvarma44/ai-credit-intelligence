from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

from jose import JWTError, jwt
from passlib.context import CryptContext


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    BASE_DIR / "users.db"
)


# --------------------------------------------------
# JWT SETTINGS
# --------------------------------------------------

SECRET_KEY = (
    "credit-risk-development-secret-key-change-this"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# --------------------------------------------------
# PASSWORD HASHING
# --------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection


# --------------------------------------------------
# CREATE TABLE
# --------------------------------------------------

def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            created_at TEXT NOT NULL

        )
        """
    )

    connection.commit()

    connection.close()


# --------------------------------------------------
# PASSWORD FUNCTIONS
# --------------------------------------------------

def hash_password(password: str):

    return pwd_context.hash(
        password
    )


def verify_password(
    plain_password: str,
    password_hash: str
):

    return pwd_context.verify(
        plain_password,
        password_hash
    )


# --------------------------------------------------
# FIND USER
# --------------------------------------------------

def get_user_by_email(email: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email.lower(),)
    )

    user = cursor.fetchone()

    connection.close()

    return user


# --------------------------------------------------
# CREATE USER
# --------------------------------------------------

def create_user(
    name: str,
    email: str,
    password: str
):

    connection = get_connection()

    cursor = connection.cursor()


    password_hash = hash_password(
        password
    )


    created_at = (
        datetime.utcnow()
        .isoformat()
    )


    try:

        cursor.execute(
            """
            INSERT INTO users (
                name,
                email,
                password_hash,
                created_at
            )

            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email.lower(),
                password_hash,
                created_at,
            )
        )

        connection.commit()

        user_id = cursor.lastrowid

    except sqlite3.IntegrityError:

        connection.close()

        raise ValueError(
            "An account with this email already exists."
        )

    finally:

        connection.close()


    return {
        "id": user_id,
        "name": name,
        "email": email.lower(),
    }


# --------------------------------------------------
# AUTHENTICATE USER
# --------------------------------------------------

def authenticate_user(
    email: str,
    password: str
):

    user = get_user_by_email(
        email
    )


    if not user:

        return None


    if not verify_password(
        password,
        user["password_hash"]
    ):

        return None


    return user


# --------------------------------------------------
# CREATE JWT
# --------------------------------------------------

def create_access_token(
    user_id: int,
    email: str
):

    expires_at = (
        datetime.utcnow()
        +
        timedelta(
            minutes=
                ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


    payload = {

        "sub": str(user_id),

        "email": email,

        "exp": expires_at,

    }


    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# --------------------------------------------------
# VERIFY JWT
# --------------------------------------------------

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM
            ]
        )

        return payload

    except JWTError:

        return None