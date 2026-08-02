# Django Authentication System

[![Live Demo](https://img.shields.io/badge/Live_Demo-Available-brightgreen)](https://django-auth.bicserdi.space/)

A comprehensive Django authentication system featuring email/password registration, Google OAuth integration, email verification, and password reset functionality. Built with Django 6.0.5, django-allauth, and Bootstrap 5 UI. Deployed on Render with Docker and PostgreSQL.

**Live Demo:** [https://django-auth.bicserdi.space/](https://django-auth.bicserdi.space/)

---

## Features

### Authentication & User Management
- **Email/Password Registration** - Secure user registration with custom user model
- **Google OAuth 2.0 Integration** - Sign in with Google using django-allauth
- **Email Verification** - Mandatory email verification before login
- **Password Reset** - Full password recovery flow
- **Login/Logout** - Secure authentication with session management
- **Custom User Model** - Extended AbstractUser with additional fields (age, country)

### Technical Implementation
- **Custom Email Backend** - Mailgun HTTP API integration for transactional emails
- **Docker Containerization** - Full development and production Docker setup
- **PostgreSQL Database** - Production-ready database with Docker Compose
- **Environment Configuration** - Secure environment variables management
- **Static Files Handling** - WhiteNoise for static file serving in production
- **CSRF Protection** - Configured trusted origins for secure form submissions

### Testing & Code Quality
- **Comprehensive Test Suite** - 50+ pytest tests covering models, forms, views, URLs, and full integration flows
- **Factory-based Test Data** - factory_boy with randomized data generation (Faker)
- **HTTP Mocking** - responses library for Mailgun API call testing
- **Static Type Checking** - mypy with django-stubs plugin across the entire codebase
- **Automated Linting** - ruff with Django-specific rules (import sorting, naming conventions)
- **CI/CD Pipeline** - GitHub Actions runs linting, type checking, and tests with coverage gates on every PR

### UI/UX
- **Bootstrap 5** - Responsive design with crispy-bootstrap5
- **django-crispy-forms** - Beautiful, clean form rendering
- **User Feedback** - Django messages framework for success/error notifications

---

## Project Structure

```
django-auth/
├── .github/
│   └── workflows/
│       └── pr-test-command.yml   # CI: lint, type-check, test, coverage
├── accounts/                  # Main authentication app
│   ├── adapters.py           # Custom allauth adapter (email as username)
│   ├── forms.py              # Registration form with extended fields
│   ├── models.py             # CustomUser model
│   ├── urls.py               # App routing
│   ├── views.py              # Authentication views
│   ├── tests/                # Test suite (pytest)
│   │   ├── conftest.py       # Fixtures (user, auth_client, social_app)
│   │   ├── factories.py      # factory_boy UserFactory
│   │   ├── test_models.py
│   │   ├── test_forms.py
│   │   ├── test_views.py
│   │   ├── test_urls.py
│   │   └── test_integration.py    # Full registration-to-login flows
│   └── templates/           # App templates
│       ├── account/          # allauth templates
│       ├── socialaccount/    # Social auth templates
│       └── home.html         # Authenticated user homepage
│
├── common/                   # Shared modules
│   ├── email_backends.py     # Mailgun HTTP API backend
│   └── tests/
│       └── test_email_backends.py  # Mailgun backend tests
│
├── config/                   # Django configuration
│   ├── settings.py          # Development settings
│   ├── settings_docker.py   # Docker development settings
│   ├── settings_production.py # Production settings
│   ├── settings_test.py     # Test settings (in-memory SQLite)
│   ├── urls.py              # Project URLs
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
│
├── templates/                # Project-level templates
│   └── base.html            # Base template with Bootstrap 5
│
├── docker-compose.yml        # Development services (web + PostgreSQL)
├── Dockerfile               # Development Docker image
├── Dockerfile.prod          # Production Docker image
├── pyproject.toml           # Pytest, ruff, mypy configuration
├── requirements.txt         # Python dependencies
├── render.yaml              # Render cloud deployment config
└── .env_*                   # Environment files
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 6.0.5, Python 3.12 |
| **Authentication** | django-allauth 65.18.0 |
| **Database** | PostgreSQL 16 (Docker), SQLite (tests) |
| **Forms** | django-crispy-forms 2.6 + crispy-bootstrap5 |
| **Email** | Mailgun HTTP API (REST) |
| **Containerization** | Docker + Docker Compose |
| **Deployment** | Render Cloud (Docker runtime) |
| **Static Files** | WhiteNoise 6.6.0 |
| **Web Server** | Gunicorn 21.2.0 |
| **OAuth Provider** | Google OAuth 2.0 |
| **Testing** | pytest 9.1, pytest-django, pytest-cov, factory_boy, Faker, responses |
| **Code Quality** | ruff 0.16 (linter), mypy 1.15 (type checker), django-stubs |
| **CI/CD** | GitHub Actions (lint → type-check → test → coverage gate ≥80%) |

---

## What I Learned

### Django & Authentication

1. **Custom User Models**
   - Extended `AbstractUser` to add custom fields (age, country)
   - Understood the importance of setting `AUTH_USER_MODEL` early in the project
   - Learned to properly migrate custom user models

2. **django-allauth Integration**
   - Implemented complete authentication flows: registration, login, logout, password reset
   - Configured email verification as mandatory before login
   - Customized signup forms with additional fields (first_name, last_name, age, country)
   - Set up email as username (no separate username required)

3. **Social Authentication**
   - Integrated Google OAuth 2.0 using django-allauth
   - Configured OAuth credentials in Google Cloud Console
   - Implemented custom adapter to use email as username for social accounts
   - Handled OAuth callback URLs and redirect URIs

4. **Email Backend Development**
   - Built custom email backend using Mailgun HTTP API
   - Understood Django's email backend architecture
   - Implemented proper error handling for API failures
   - Supported text, HTML, CC, BCC, attachments, and reply-to headers

### DevOps & Deployment

5. **Docker & Containerization**
   - Created multi-stage Dockerfiles for development and production
   - Configured Docker Compose with separate web and database services
   - Set up PostgreSQL container with persistent volumes
   - Managed environment variables securely across containers

6. **Production Deployment**
   - Deployed to Render Cloud with Docker
   - Configured production settings (DEBUG=False, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS)
   - Set up PostgreSQL database in production
   - Implemented WhiteNoise for static file serving
   - Configured Gunicorn as production WSGI server

7. **Environment Management**
   - Used python-dotenv for local development
   - Separated development, Docker, and production environments
   - Secured sensitive credentials (SECRET_KEY, database passwords, API keys)
   - Configured dj-database-url for database connection parsing

### UI & User Experience

8. **Bootstrap 5 Integration**
   - Implemented responsive design with Bootstrap 5
   - Used crispy-bootstrap5 for form styling
   - Created reusable base template with blocks for inheritance
   - Implemented user feedback with Django messages framework

9. **Form Customization**
   - Extended allauth's default forms
   - Added custom validation and fields
   - Customized form labels and help text
   - Implemented proper error display

### Security Best Practices

10. **Authentication Security**
    - Enforced email verification before allowing login
    - Implemented secure password reset flow
    - Configured CSRF protection with trusted origins
    - Used Django's built-in authentication decorators (@login_required, @require_POST)

11. **Environment Security**
    - Never committed secrets to version control
    - Used environment variables for all sensitive data
    - Configured separate settings files for different environments
    - Set up proper ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS

### Testing & Code Quality

12. **pytest & Test Architecture**
    - Structured tests by domain (models, forms, views, URLs, integration) using pytest discovery
    - Used `conftest.py` fixtures for reusable test setup (user, verified_user, auth_client)
    - Leveraged `pytest-django` for Django ORM integration and `pytest-cov` for coverage
    - Built `factory_boy` factories with Faker for randomized, realistic test data
    - Mocked external HTTP calls with `responses` library to test Mailgun API integration
    - Ran tests against in-memory SQLite for speed without external dependencies

13. **Static Type Checking (mypy)**
    - Configured mypy with `django-stubs` for full Django type inference
    - Added type annotations across all views, signals, and model methods
    - Understood how type stubs catch real-world Django bugs at analysis time
    - Used per-file `type: ignore` comments only where strictly necessary

14. **Automated Linting (ruff)**
    - Configured ruff with Django-aware rules (DJ, N, I import sorting)
    - Enforced consistent import ordering, naming conventions, and line length
    - Learned to integrate ruff as a pre-commit gate via CI rather than a manual step

15. **CI/CD with GitHub Actions**
    - Designed a workflow that runs lint → type check → test → coverage in sequence
    - Published JUnit test results as check run annotations on every PR
    - Added coverage summaries to the workflow run page via `GITHUB_STEP_SUMMARY`
    - Set an 80% coverage threshold to prevent untested code from merging
    - Ran CI on every pull request to catch regressions before merge

---

## Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL (optional for local development)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bicskow/django-auth.git
   cd django-auth
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create and apply migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Run development server:**
   ```bash
   python manage.py runserver
   ```

   Access at: http://localhost:8000

5. **Run tests:**
   ```bash
   pytest --cov=accounts --cov=common --cov-report=term-missing
   ```

6. **Lint & type-check:**
   ```bash
   ruff check .
   mypy .
   ```

### Docker Development

1. **Start services:**
   ```bash
   docker compose up
   ```

2. **Run migrations in container:**
   ```bash
   docker compose exec web python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

   Access at: http://localhost:8000

### Production Deployment

The project is configured for deployment on Render Cloud:

1. Set environment variables in Render dashboard
2. Connect PostgreSQL database
3. Configure domain and SSL
4. Deploy using the provided `Dockerfile.prod` and `render.yaml`

---

## Configuration

### Environment Variables

Create `.env` file based on `.env_template`:

```bash
# Django
DJANGO_SETTINGS_MODULE=config.settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Email (Mailgun)
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_DOMAIN=your-mailgun-domain
DEFAULT_FROM_EMAIL=No Reply <noreply@your-domain.com>

# Site
SITE_DOMAIN=localhost:8000
SITE_NAME=My Django Project

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# CSRF
CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

---

## API & Service Integrations

### Google OAuth 2.0
1. Create project in Google Cloud Console
2. Enable Google+ API
3. Create OAuth 2.0 credentials
4. Add authorized redirect URIs: `https://your-domain.com/accounts/google/login/callback/`

### Mailgun Email API
1. Create Mailgun account
2. Verify domain
3. Get API key
4. Configure DNS records (MX, SPF, DKIM)

---

## Project Highlights

### Custom Email Backend Implementation
The `MailgunBackend` class in `common/email_backends.py` demonstrates:
- Extending Django's `BaseEmailBackend`
- HTTP API integration instead of SMTP
- Support for all email features (attachments, HTML, CC, BCC)
- Proper error handling and status code checking

### Authentication Flow
1. User registers with email, password, and optional fields
2. Verification email sent via Mailgun
3. User clicks verification link
4. Email address marked as verified in database
5. User can now login (verified email required)
6. Google OAuth users automatically have verified email

### Security Measures
- Email verification required before login
- CSRF protection with trusted origins
- Secure password hashing (Django default)
- HTTPS enforced in production
- Sensitive data never in version control

---


## License

MIT License - see LICENSE file for details.

---

## Contact

For questions or feedback about this project, please contact me.

**Live Demo:** [https://django-auth.bicserdi.space/](https://django-auth.bicserdi.space/)
