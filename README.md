# Mini CRM

Lead management system built with FastAPI + SQLAlchemy + MySQL.

## Features

- User authentication (JWT access/refresh tokens)
- Lead CRUD (create, read, update, delete)
- Lead statuses: New, Contacted, Qualified, Won, Lost
- Pagination, search, status filter, sorting
- Activity history per lead
- Dashboard statistics
- HTML frontend served via CORS

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy 2.0, PyMySQL
- **Database:** MySQL
- **Auth:** JWT (python-jose), Argon2 password hashing (passlib)
- **Frontend:** Vanilla HTML/CSS/JS

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv python-jose passlib argon2-cffi
```

3. Create a `.env` file in the project root:
```
DB_USERNAME=root
DB_PASS=your_password
DB_NAME=minicrm
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

4. Create the MySQL database:
```sql
CREATE DATABASE minicrm;
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

6. Open http://localhost:8000 for the frontend or http://localhost:8000/docs for API documentation.

## Creating First User

The first user (with role "boss") must be created directly in the database. Use a Python script to hash the password:

```python
from app.utils.securty import hash_password
print(hash_password("your_password"))
```

Then insert:
```sql
INSERT INTO Login (username, password, role) VALUES ('admin', 'hashed_password_here', 'boss');
```

After that, use the "boss" account to create additional users via `/create_login/newlogin`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /login/login | Authenticate and get tokens |
| POST | /login/refresh | Refresh access token |
| GET | /login/me | Get current user |
| POST | /create_login/newlogin | Create new user (boss only) |
| POST | /leads/ | Create a lead |
| GET | /leads/ | List leads (paginated, filterable) |
| GET | /leads/{id} | Get lead details |
| PUT | /leads/{id} | Update lead |
| DELETE | /leads/{id} | Delete lead |
| GET | /leads/{id}/activities | Get lead activity history |
| GET | /dashboard/stats | Get dashboard statistics |

## Architecture

- `app/models/` - SQLAlchemy ORM models (Login, Lead, Activity)
- `app/scheme/` - Pydantic schemas for request/response validation
- `app/routers/` - API route handlers
- `app/utils/` - Security utilities (JWT, password hashing)
- `app/database/` - Database connection and Base model
- `static/` - Frontend HTML

The app uses JWT-based authentication with access and refresh tokens. Leads support full CRUD with pagination, search across multiple fields, status filtering, and sorting. Activity tracking logs all lead creation and status changes.
