# Django Student Management — Technical Notes

## Overview

A Django 6 student management application with server-rendered CRUD pages, a Django REST Framework API, and a Django admin site.

## Architecture

```text
Browser
  ├─ /students/          server-rendered list/create/detail/update/delete
  ├─ /admin/             Django admin
  └─ /api/students/      DRF viewset
        └─ PostgreSQL (preferred) or SQLite (development fallback)
```

## Folder structure

```text
backend/
  manage.py
  studentmgmt/          Django project settings and root URLs
  students/
    models.py           Student model
    forms.py            Student form
    views.py            Class-based CRUD views
    serializers.py      DRF serializer
    api.py              StudentViewSet
    urls.py             Student page routes
    tests/              Test suite
  requirements.txt
infra/                  Docker and Jenkins configuration
database/               Database notes
```

## Data model

`Student` fields:

- `name`
- `email` (unique)
- `age` (minimum 1)
- `course` (CS, ENG, MATH, PHY, BIO)
- `enrollment_date` (automatic)

## Routes

| Route | Purpose |
|---|---|
| `/` | Redirects to `/students/` |
| `/students/` | Paginated student list |
| `/students/create/` | Create student |
| `/students/<id>/` | Student detail |
| `/students/<id>/update/` | Update student |
| `/students/<id>/delete/` | Delete student |
| `/admin/` | Django admin |
| `/api/students/` | REST API |

## Setup

```powershell
cd backend
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

Create an admin account if needed:

```powershell
python manage.py createsuperuser
```

## Tests

```powershell
cd backend
pytest
```

Verified result: **35/35 tests passed** on 2026-11-09.

## Verification evidence

| Check | Result |
|---|---|
| `python manage.py check` | No issues |
| `pytest` | 35/35 passed |
| `/` | Redirects to `/students/` |
| `/admin/` | HTTP 200 |

## Configuration

Use `backend/.env` (see `.env.example`). The sample used port `5433`; the local workspace uses PostgreSQL on `5432`.

```dotenv
DB_ENGINE=django.db.backends.postgresql
DB_NAME=studentmgmt
DB_USER=studentuser
DB_PASSWORD=studentpass
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
```

## Limitations

- Docker Compose and the Jenkins pipeline were not executed during verification.
- PostgreSQL is preferred, but a development `db.sqlite3` file is present.
- `DEBUG=True` and the sample secret key are development-only.
- The admin account must be created locally; credentials are not committed.
