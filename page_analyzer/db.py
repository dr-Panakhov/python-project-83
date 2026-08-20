import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))


def get_all_urls():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("""
                SELECT DISTINCT ON (urls.id)
                    urls.id,
                    urls.name,
                    url_checks.created_at AS last_check,
                    url_checks.status_code
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                ORDER BY urls.id DESC, url_checks.id DESC
            """)
            return cur.fetchall()


def find_url_by_name(name):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT id, name FROM urls WHERE name = %s", (name,))
            return cur.fetchone()


def find_url_by_id(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            return cur.fetchone()


def add_url(name):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                (name,)
            )
            new_id = cur.fetchone().id
            conn.commit()
            return new_id


def get_url_checks(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC",
                (url_id,)
            )
            return cur.fetchall()


def add_url_check(url_id, status_code, h1, title, description):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """INSERT INTO url_checks
                   (url_id, status_code, h1, title, description)
                   VALUES (%s, %s, %s, %s, %s)""",
                (url_id, status_code, h1, title, description)
            )
            conn.commit()
