# ATS Lite — Job Application Tracking System

> Built with Django 4.2 + Django REST Framework + Tailwind CSS

A production-ready Applicant Tracking System (ATS) featuring job management, candidate applications, intelligent skill-matching scoring, and a real-time notification system.

---

## 🚀 Live Features

| Feature | Status |
|---|---|
| Job CRUD API | ✅ |
| Candidate Application | ✅ |
| Skill Match Scoring (%) | ✅ |
| Ranked Candidate List | ✅ |
| Notification System | ✅ |
| Mark Read / Unread | ✅ |
| Resume Upload | ✅ |
| Search & Filter | ✅ |
| Pagination | ✅ |
| Token + Session Auth | ✅ |
| Admin Panel | ✅ |
| Tailwind UI | ✅ |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Django 4.2, Django REST Framework 3.14
- **Database:** SQLite (dev) — swap to PostgreSQL with one config change
- **Frontend:** Django Templates + Tailwind CSS CDN
- **Auth:** Session (browser) + Token (API clients)

---

## ⚡ Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/ats-lite.git
cd ats-lite

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations jobs candidates notifications
python manage.py migrate
```

### 3. Create Superuser (Recruiter Account)

```bash
python manage.py createsuperuser
```

### 4. Load Sample Data (Optional)

```bash
python manage.py seed_data
```

### 5. Run Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
ats_lite/
├── ats_lite/           ← Django project config
│   ├── settings.py
│   ├── urls.py         ← Root URL dispatcher
│   ├── api_urls.py     ← All /api/v1/ routes
│   └── auth_views.py   ← Login/Register views
│
├── jobs/               ← Job listings app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py        ← DRF ViewSet
│   └── template_views.py
│
├── candidates/         ← Candidates & Applications
│   ├── models.py
│   ├── utils.py        ← ⭐ Skill matching algorithm
│   ├── serializers.py
│   └── views.py
│
├── notifications/      ← Notification system
│   ├── models.py
│   └── views.py
│
└── templates/          ← HTML + Tailwind UI
```

---

## 🔌 API Documentation

### Authentication

```bash
# Get API token
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -d "username=admin&password=yourpassword"
```

Include in all API requests:
```
Authorization: Token <your-token>
```

---

### Jobs API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/jobs/` | List all jobs |
| POST | `/api/v1/jobs/` | Create job |
| GET | `/api/v1/jobs/{id}/` | Job detail |
| PUT | `/api/v1/jobs/{id}/` | Update job |
| DELETE | `/api/v1/jobs/{id}/` | Delete job |
| GET | `/api/v1/jobs/?search=python` | Search jobs |
| GET | `/api/v1/jobs/{id}/applicants/` | Ranked applicants |

**Create Job:**
```bash
curl -X POST http://localhost:8000/api/v1/jobs/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "Build scalable APIs",
    "required_skills": "Python, Django, PostgreSQL, Docker"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Senior Python Developer",
  "required_skills": "Python, Django, PostgreSQL, Docker",
  "skills_list": ["python", "django", "postgresql", "docker"],
  "is_active": true,
  "created_at": "2025-01-01T10:00:00Z"
}
```

---

### Candidates API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/candidates/apply/{job_id}/` | Apply to job |
| GET | `/api/v1/candidates/ranked/{job_id}/` | Ranked list |
| GET | `/api/v1/candidates/ranked/{job_id}/?min_score=50` | Filter by score |
| PATCH | `/api/v1/candidates/application/{id}/status/` | Update status |
| GET | `/api/v1/candidates/` | List all candidates |

**Apply to a Job:**
```bash
curl -X POST http://localhost:8000/api/v1/candidates/apply/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "skills": "Python, Django, REST API",
    "cover_letter": "I am excited about this role..."
  }'
```

**Response:**
```json
{
  "message": "Application submitted successfully!",
  "application_id": 5,
  "match_score": 75.0,
  "match_details": {
    "matched": ["django", "python", "rest api"],
    "missing": ["docker", "postgresql"],
    "extra": []
  }
}
```

**Ranked Candidates:**
```bash
GET /api/v1/candidates/ranked/1/
```
```json
{
  "job_title": "Senior Python Developer",
  "total": 3,
  "candidates": [
    {
      "name": "Alice Smith",
      "match_score": 100.0,
      "match_label": "Perfect Match",
      "matched_skills": ["django", "docker", "postgresql", "python"]
    },
    {
      "name": "Jane Doe",
      "match_score": 75.0,
      "match_label": "Good Match",
      "matched_skills": ["django", "python", "rest api"],
      "missing_skills": ["docker", "postgresql"]
    }
  ]
}
```

---

### Notifications API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/notifications/` | All notifications |
| GET | `/api/v1/notifications/?unread=true` | Unread only |
| PATCH | `/api/v1/notifications/{id}/read/` | Mark as read |
| PATCH | `/api/v1/notifications/{id}/unread/` | Mark as unread |
| POST | `/api/v1/notifications/mark-all-read/` | Mark all read |

---

## 🧠 Skill Matching Logic

```
score = (matched_skills ÷ total_required_skills) × 100
```

| Score | Label |
|-------|-------|
| 100% | Perfect Match |
| 76–99% | Strong Match |
| 51–75% | Good Match |
| 26–50% | Partial Match |
| 0–25% | Poor Match |

Edge cases handled: empty skills, duplicate skills, case-insensitive matching.

---

## 🐘 Switch to PostgreSQL

In `settings.py`, replace DATABASES:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': '5432',
    }
}
```

Add `psycopg2-binary` to `requirements.txt` and run `pip install psycopg2-binary`.

---

## 🌐 Deployment (Render.com)

1. Push to GitHub
2. Create new Web Service on Render
3. Build Command: `pip install -r requirements.txt && python manage.py migrate`
4. Start Command: `gunicorn ats_lite.wsgi`
5. Set environment variables: `SECRET_KEY`, `DEBUG=False`

---

## 🔑 Environment Variables

Create a `.env` file (never commit this):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=ats_lite
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
```

---

## 👨‍💻 Admin Panel

Visit: `http://127.0.0.1:8000/admin/`
Login with your superuser credentials to manage all data directly.

---


### 👤 User Login
- UserName: shubh
- Password: Shubh@2002

### 👤 Superuser Login
- UserName: Admin
- Password: 1234

