# project_django_student_management

## Django Student Management

A Django 6 + Django REST Framework student management system with a PostgreSQL backend, admin site, and pytest test suite.

- Original location: `D:\Computers Files\4th sem\Cloud computing\Code with rabin`
- Working copy: `D:\PROJECTS_READY\project_django_student_management`
- Stack: Python 3, Django 6, Django REST Framework, PostgreSQL/SQLite, pytest

## Folder layout

```text
project_django_student_management/
  backend/    Django project, students app, tests, Docker/Jenkins files
  database/   Database notes
  docs/       Project documentation
```

## Setup and run

```powershell
cd backend
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
pytest
python manage.py runserver
```

Environment (`backend/.env`):

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

The sample `.env` used port `5433`; change it to your PostgreSQL port (the local workspace uses `5432`).

## Verified status (2026-11-09)

- [x] `python manage.py check` completed with no issues
- [x] `pytest` passed 35/35 tests
- [x] `/` redirects correctly
- [x] `/admin/` returned HTTP 200
- [ ] Docker Compose/Jenkins pipeline not run during verification

## Notes and limitations

- PostgreSQL is preferred; a SQLite database (`db.sqlite3`) is present from development.
- The Django admin account must be created with `python manage.py createsuperuser` if it does not exist.
- `DEBUG=True` and the sample secret key are development-only.
- Do not commit `.env`, `db.sqlite3`, coverage files, or static build output.

## Troubleshooting

- **Database connection refused**: verify PostgreSQL is running and `DB_PORT` matches (5432 locally).
- **Missing tables**: run `python manage.py migrate`.
- **Tests fail on database permissions**: use a test database/user with create/drop privileges, or set a SQLite test configuration.
- **Admin login unknown**: create a superuser with `python manage.py createsuperuser`.
