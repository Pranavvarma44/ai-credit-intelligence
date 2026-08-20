import os

import psycopg2
from psycopg2.extras import RealDictCursor

from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from dotenv import load_dotenv


# ==================================================
# ENVIRONMENT
# ==================================================

load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


# ==================================================
# JWT
# ==================================================

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-secret-change-this"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# ==================================================
# PASSWORD HASHING
# ==================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_connection():

    if not DATABASE_URL:

        raise RuntimeError(
            "DATABASE_URL is not configured."
        )

    return psycopg2.connect(
        DATABASE_URL
    )


# ==================================================
# INITIALIZE DATABASE
# ==================================================

def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id SERIAL PRIMARY KEY,

            name VARCHAR(255) NOT NULL,

            email VARCHAR(255) UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            created_at TIMESTAMP NOT NULL

        );
        """
    )

    connection.commit()

    cursor.close()

    connection.close()


# ==================================================
# PASSWORD VALIDATION
# ==================================================

def validate_password(password: str):

    if not password:

        raise ValueError(
            "Password cannot be empty."
        )

    if len(
        password.encode("utf-8")
    ) > 72:

        raise ValueError(
            "Password cannot be longer than 72 bytes."
        )


# ==================================================
# HASH PASSWORD
# ==================================================

def hash_password(password: str):

    validate_password(password)

    return pwd_context.hash(
        password
    )


# ==================================================
# VERIFY PASSWORD
# ==================================================

def verify_password(
    plain_password,
    password_hash
):

    validate_password(
        plain_password
    )

    return pwd_context.verify(
        plain_password,
        password_hash
    )


# ==================================================
# GET USER BY EMAIL
# ==================================================

def get_user_by_email(email: str):

    connection = get_connection()

    cursor = connection.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            password_hash,
            created_at
        FROM users
        WHERE email = %s
        """,
        (email.lower(),)
    )

    user = cursor.fetchone()

    cursor.close()

    connection.close()

    return user


# ==================================================
# CREATE USER
# ==================================================

def create_user(
    name: str,
    email: str,
    password: str
):

    password_hash = hash_password(
        password
    )

    connection = get_connection()

    cursor = connection.cursor(
        cursor_factory=RealDictCursor
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

            VALUES (
                %s,
                %s,
                %s,
                %s
            )

            RETURNING id, name, email
            """,
            (
                name,
                email.lower(),
                password_hash,
                datetime.utcnow()
            )
        )

        user = cursor.fetchone()

        connection.commit()

        return dict(user)

    except psycopg2.errors.UniqueViolation:

        connection.rollback()

        raise ValueError(
            "An account with this email already exists."
        )

    finally:

        cursor.close()

        connection.close()


# ==================================================
# AUTHENTICATE USER
# ==================================================

def authenticate_user(
    email: str,
    password: str
):

    user = get_user_by_email(
        email
    )

    if not user:

        return None

    try:

        valid = verify_password(
            password,
            user["password_hash"]
        )

    except ValueError:

        return None

    if not valid:

        return None

    return user


# ==================================================
# CREATE JWT
# ==================================================

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

        "exp": expires_at

    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==================================================
# VERIFY JWT
# ==================================================

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