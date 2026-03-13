---
name: flask-workflow
description: Flask framework workflow guidelines. Activate when working with Flask projects, flask run, or Flask-specific patterns.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Flask Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Run dev | Flask CLI | `flask run --debug` |
| Test | pytest | `uv run pytest` |
| Lint | Ruff | `uv run ruff check .` |
| Format | Ruff | `uv run ruff format .` |
| Migrate | Flask-Migrate | `flask db upgrade` |
| Shell | Flask CLI | `flask shell` |

---

## Application Factory Pattern

All Flask applications MUST use the application factory pattern.

```python
# app/__init__.py
from flask import Flask

def create_app(config_name: str = "default") -> Flask:
    """Application factory function."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.main import main_bp
    from app.auth import auth_bp
    from app.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    # Register error handlers
    register_error_handlers(app)

    return app
```

---

## Blueprint Organization

Routes MUST be organized using Blueprints. NEVER define routes directly on the app object.

### Directory Structure

```
app/
├── __init__.py          # create_app() factory
├── extensions.py        # Extension instances
├── models/              # SQLAlchemy models
│   ├── __init__.py
│   └── user.py
├── main/                # Main blueprint
│   ├── __init__.py      # Blueprint definition
│   ├── routes.py        # Route handlers
│   └── forms.py         # WTForms (if used)
├── auth/                # Auth blueprint
│   ├── __init__.py
│   ├── routes.py
│   └── forms.py
└── api/                 # API blueprint
    ├── __init__.py
    ├── routes.py
    └── schemas.py       # Marshmallow/Pydantic schemas
```

### Blueprint Definition

```python
# app/main/__init__.py
from flask import Blueprint

main_bp = Blueprint("main", __name__)

from app.main import routes  # noqa: E402, F401
```

---

## Configuration

Configuration MUST be loaded from environment variables for secrets. Configuration classes SHOULD be used for different environments.

```python
# config.py
import os
from pathlib import Path

basedir = Path(__file__).parent


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-prod"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """Initialize application-specific config."""
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
        f"sqlite:///{basedir / 'dev.db'}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    @staticmethod
    def init_app(app):
        # Production-specific initialization
        pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
```

---

## Extensions Pattern

Extensions MUST be instantiated in a separate module without app binding, then initialized in the factory.

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
```

---

## Flask-SQLAlchemy Patterns

### Model Definition

```python
# app/models/user.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return db.session.get(User, int(user_id))
```

### Query Patterns

```python
# RECOMMENDED: Use db.session for queries
user = db.session.get(User, user_id)  # By primary key
users = db.session.scalars(db.select(User).filter_by(active=True)).all()

# SHOULD avoid deprecated Model.query
# user = User.query.get(user_id)  # Deprecated
```

---

## Flask-Migrate

Database migrations MUST use Flask-Migrate. NEVER modify the database schema manually.

```bash
# Initialize migrations (once)
flask db init

# Create migration after model changes
flask db migrate -m "Add user table"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade
```

---

## Flask-Login Authentication

```python
# app/auth/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.models.user import User


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        user = db.session.scalar(
            db.select(User).filter_by(email=request.form["email"])
        )
        if user and user.check_password(request.form["password"]):
            login_user(user, remember=request.form.get("remember"))
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.index"))
        flash("Invalid email or password")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
```

---

## Request and Application Context

### Application Context

Use `with app.app_context():` when accessing app-bound resources outside request handling.

```python
# CLI commands, background tasks, etc.
with app.app_context():
    db.create_all()
    user = db.session.get(User, 1)
```

### Request Context

Request-specific data (g, request, session) MUST only be accessed within request context.

```python
from flask import g, request

@app.before_request
def before_request():
    g.user = current_user
    g.locale = request.accept_languages.best_match(["en", "es"])
```

---

## Error Handlers

Error handlers SHOULD be registered in the application factory.

```python
# app/errors.py
from flask import render_template, jsonify, request


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Not found"}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal server error"}), 500
        return render_template("errors/500.html"), 500
```

---

## Testing with Test Client

Tests MUST use pytest fixtures. Test configuration MUST use TestingConfig.

```python
# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
```

```python
# tests/test_auth.py
def test_login_page(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_success(client, user):
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
```

---

## API Routes

API blueprints SHOULD return JSON responses and use proper HTTP status codes.

```python
# app/api/routes.py
from flask import jsonify, request
from app.api import api_bp
from app.models.user import User


@api_bp.route("/users/<int:user_id>")
def get_user(user_id: int):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    })


@api_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("email"):
        return jsonify({"error": "Email required"}), 400

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id}), 201
```

---

## CLI Commands

Custom CLI commands SHOULD be defined using `@app.cli.command()` or Click groups.

```python
# app/cli.py
import click
from app.extensions import db


def register_cli(app):
    @app.cli.command()
    def initdb():
        """Initialize the database."""
        db.create_all()
        click.echo("Database initialized.")

    @app.cli.command()
    @click.argument("email")
    @click.password_option()
    def create_admin(email, password):
        """Create an admin user."""
        from app.models.user import User
        user = User(email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Admin {email} created.")
```

---

## Security Checklist

- [ ] SECRET_KEY MUST be set from environment in production
- [ ] CSRF protection MUST be enabled for forms
- [ ] Passwords MUST be hashed with werkzeug.security
- [ ] SQL queries MUST use parameterized statements (SQLAlchemy handles this)
- [ ] User input MUST be validated before use
- [ ] Debug mode MUST NOT be enabled in production
