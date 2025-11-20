.PHONY: sync install-hooks format lint check pre-commit clean setup dev compose-up compose-down docker-logs docker-build docker-rebuild

sync:
	uv sync --extra dev

install-hooks:
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg

format:
	uv run ruff format .

lint:
	uv run ruff check --fix .

check:
	uv run ruff check .
	uv run ruff format --check .

pre-commit:
	uv run pre-commit run --all-files

commit:
	uv run cz commit

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .venv

setup: sync install-hooks
	@echo "Project setup completed"

dev:
	uv run uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload

compose-up:
	COMPOSE_BAKE=true docker-compose up -d

compose-down:
	docker-compose down

docker-logs:
	docker-compose logs -f api

docker-build:
	docker-compose up --build

docker-rebuild:
	docker-compose build --no-cache
	docker-compose up -d

migrate:
	uv run alembic revision --autogenerate -m "$(msg)"

upgrade:
	uv run alembic upgrade head

downgrade:
	uv run alembic downgrade -1

current:
	uv run alembic current

history:
	uv run alembic history
