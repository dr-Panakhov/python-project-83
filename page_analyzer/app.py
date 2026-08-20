import os
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

from page_analyzer import db
from page_analyzer.url_validator import validate, normalize
from page_analyzer.parser import parse_html

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def urls_post():
    url = request.form.get('url')

    errors = validate(url)
    if errors:
        flash(errors[0], 'danger')
        return render_template('index.html', url=url), 422

    normalized_url = normalize(url)
    existing_url = db.find_url_by_name(normalized_url)

    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_show', id=existing_url.id))

    new_id = db.add_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_show', id=new_id))


@app.route('/urls')
def urls_index():
    urls = db.get_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def url_show(id):
    url = db.find_url_by_id(id)

    if not url:
        return "Not Found", 404

    checks = db.get_url_checks(id)
    return render_template('url.html', url=url, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks_post(id):
    url = db.find_url_by_id(id)

    if not url:
        return "Not Found", 404

    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_show', id=id))

    parsed_data = parse_html(response.text)
    db.add_url_check(
        id,
        response.status_code,
        parsed_data['h1'],
        parsed_data['title'],
        parsed_data['description']
    )

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_show', id=id))
