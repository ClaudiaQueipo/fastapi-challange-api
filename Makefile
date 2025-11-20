.PHONY: sync install-hooks format lint check pre-commit clean setup

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
