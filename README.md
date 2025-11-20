# FastAPI Challenge API

A simple API for managing posts and tags with user authentication.

## Requirements
- uv installed.
- make for easy commands.
- Docker and Docker Compose for deployment.
- PostgreSQL as database.

## Architecture
The project follows modular architecture principles, with each feature in its own module (auth, posts, tags). Core has shared utilities.

Basic structure:
- app/core/: Shared config (DB, exceptions, schemas).
- app/auth/: Authentication (JWT, register, login).
- app/posts/: Post management.
- app/tags/: Tag management.
- Migrations with Alembic.
- Docker for containers.

## Installation
1. Clone the repo and enter the directory.
2. Run `make setup` to install dependencies.
3. Copy `.env.example` to `.env` and configure the DB.
4. Run `make upgrade` for migrations.
5. Start with `make dev` or `docker-compose up`.

## Endpoints
- Auth: POST /api/v1/auth/register, POST /api/v1/auth/login.
- Posts: Full CRUD, paginated GET. Only owner can edit/delete.
- Tags: Similar to posts.

Use Bearer token for protected endpoints. Only owners manage their resources.

## Development
- Linting: `make lint`.
- Formatting: `make format`.
- Migrations: `make migrate msg="..."` then `make upgrade`.

## Deployment
fastapi-challenge-api/
├── app/
│   ├── core/                    # Shared application components
│   │   ├── db.py                # Database connection and session
│   │   ├── exception_handlers.py # Global exception handlers
│   │   ├── exceptions.py        # Custom exception classes
│   │   ├── middleware.py        # Custom middleware
│   │   ├── mixins.py            # SQLAlchemy mixins (CRUD, timestamps)
│   │   ├── schemas.py           # Shared Pydantic schemas (e.g., PaginatedResponse)
│   │   └── settings.py          # Application settings
│   ├── auth/                    # Authentication module
│   │   ├── dependencies.py      # Auth-specific FastAPI dependencies
│   │   ├── models.py            # User model
│   │   ├── routes.py            # Auth endpoints (register, login)
│   │   ├── schemas.py           # Auth schemas (UserCreate, Token)
│   │   └── services.py          # Auth business logic (hashing, JWT)
│   ├── posts/                   # Posts module
│   │   ├── models.py            # Post model
│   │   ├── routes.py            # Post endpoints (CRUD)
│   │   ├── schemas.py           # Post schemas
│   │   └── services.py          # Post business logic
│   └── tags/                    # Tags module
│       ├── models.py            # Tag model
│       ├── routes.py            # Tag endpoints (CRUD)
│       ├── schemas.py           # Tag schemas
│       └── services.py          # Tag business logic
│   ├── app.py                   # FastAPI app configuration
│   └── main.py                  # Entry point
├── migrations/                  # Alembic database migrations
├── pyproject.toml               # Project dependencies and config
├── uv.lock                      # Dependency lock file
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Multi-container setup
├── Makefile                     # Automation scripts
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

### Key Principles
- **Modularity**: Each feature is self-contained with its own models, schemas, services, and routes.
- **Dependency Injection**: FastAPI dependencies are defined in `dependencies.py` per module.
- **Shared Core**: Common utilities (DB, exceptions, schemas) in `core/`.
- **Security**: JWT-based authentication with owner-based permissions.
- **Pagination**: Standardized paginated responses with `total` count.

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd fastapi-challenge-api
   ```

2. **Install dependencies**:
   ```bash
   make setup
   ```

3. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run database migrations**:
   ```bash
   make upgrade
   ```

5. **Start the application**:
   ```bash
   make dev  # or make compose-up
   ```
