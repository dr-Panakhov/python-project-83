# Анализатор страниц (Page Analyzer)

### Hexlet Python Project #3

[![Actions Status](https://github.com/dr-Panakhov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/dr-Panakhov/python-project-83/actions)
[![Lint Status](https://github.com/dr-Panakhov/python-project-83/actions/workflows/lint.yml/badge.svg)](https://github.com/dr-Panakhov/python-project-83/actions)

**Ссылка на сайт:** [https://python-project-83-j5bd.onrender.com](https://python-project-83-j5bd.onrender.com)

---

## Описание

**Анализатор страниц** — это полноценное SEO-веб-приложение на фреймворке Flask. Приложение позволяет добавлять сайты для анализа, проверять их доступность (HTTP-статус) и автоматически извлекать ключевые SEO-теги (`<h1>`, `<title>`, `<meta name="description">`).

---

## Технологии
- **Python 3.10+**
- **Flask**
- **PostgreSQL / psycopg2**
- **BeautifulSoup4**
- **Requests**
- **Bootstrap 5**
- **uv / Hatchling**
- **Ruff** (Линтер)

---

## Требования
- Python >= 3.10
- PostgreSQL
- uv package manager

---

## Инструкция по установке и запуску

### 1. Клонирование репозитория
```bash
git clone [https://github.com/dr-Panakhov/python-project-83.git](https://github.com/dr-Panakhov/python-project-83.git)
cd python-project-83
```

### 2. Установка зависимостей
```bash
make install
```

### 3. Настройка переменных окружения
Создайте файл `.env` в корне проекта:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/page_analyzer
```

### 4. Создание базы данных
```bash
psql -a -d postgresql://postgres:postgres@localhost:5432/page_analyzer -f database.sql
```

### 5. Запуск сервера для разработки
```bash
make dev
```
После этого откройте браузер: `http://localhost:5000`

### 6. Проверка кода линтером
```bash
make lint
```
