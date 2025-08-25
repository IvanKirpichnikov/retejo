lint:
    ruff check
    mypy
    codespell src examples tests
    bandit -c pyproject.toml -r src examples
    flake8 --select WPS src
    slotscheck src  # Можно скипнуть

format:
    ruff format

tests:
    pytest tests
