## FastAPI Diang Challange

## Project requirements
- YOU must have uv installed.
- Also install make for easy and faster command execution for the pre-configured task commands

## Project Architecture
Based on **Screaming Architecture** and **Vertical Slicing** principles to maintain clear separation of concerns and feature-based organization.

```
fastapi-challange-api/
├── app/
│   ├── __init__.py
│   ├── core/                    # Core application configuration
│   │   ├── __init__.py
│   │   ├── settings.py          # Pydantic settings
│   │   ├── config.py            # Additional config
│   │   ├── database.py          # Database setup
│   │   ├── security.py          # Security utilities
│   │   ├── dependencies.py      # FastAPI dependencies
│   │   └── exceptions.py        # Custom exceptions
│   ├── auth/                    # Authentication feature
│   │   ├── __init__.py
│   │   ├── models.py            # Auth database models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── services.py          # Business logic
│   │   ├── routes.py            # API endpoints
│   │   └── dependencies.py      # Auth-specific dependencies
│   ├── posts/                   # Posts feature
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   ├── routes.py
│   │   └── dependencies.py
│   └── comments/                # Comments feature
│       ├── __init__.py
│       ├── models.py
│       ├── schemas.py
│       ├── services.py
│       ├── routes.py
│       └── dependencies.py
├── main.py                      # FastAPI app entry point
├── pyproject.toml              # Project dependencies (UV)
├── uv.lock                     # Lock file
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── .dockerignore              # Docker ignore rules
├── .env                       # Environment variables (not in git)
├── .env.example               # Environment variables template
├── Makefile                   # Task automation
└── README.md                  # This file
```
