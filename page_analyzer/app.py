import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime
from urllib.parse import urlparse
import validators
import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def urls_post():
    url = request.form.get('url')

    if not validators.url(url) or len(url) > 255:
        flash('Некорректный URL', 'danger')
        return render_template('index.html', url=url), 422

    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT id FROM urls WHERE name = %s", (normalized_url,))
            existing_url = cur.fetchone()

            if existing_url:
                flash('Страница уже существует', 'info')
                return redirect(url_for('url_show', id=existing_url.id))

            created_at = datetime.now()
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (normalized_url, created_at)
            )
            new_id = cur.fetchone().id
            conn.commit()

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_show', id=new_id))


@app.route('/urls')
def urls_index():
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
            urls = cur.fetchall()

    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def url_show(id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            url = cur.fetchone()

            if not url:
                return "Not Found", 404
            
            cur.execute("SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC", (id,))
            checks = cur.fetchall()

    return render_template('url.html', url=url, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks_post(id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT id, name FROM urls WHERE id = %s", (id,))
            url = cur.fetchone()
            
            if not url:
                return "Not Found", 404

            try:
                response = requests.get(url.name)
                response.raise_for_status()
            except requests.exceptions.RequestException:
                flash('Произошла ошибка при проверке', 'danger')
                return redirect(url_for('url_show', id=id))

            created_at = datetime.now()
            status_code = response.status_code
            
            cur.execute(
                """INSERT INTO url_checks (url_id, status_code, created_at) 
                   VALUES (%s, %s, %s)""",
                (id, status_code, created_at)
            )
            conn.commit()

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_show', id=id))
