lint:
    ruff check
    mypy
    codespell src examples tests
    bandit -c pyproject.toml -r src examples
    slotscheck src  # Можно скипнуть

format:
    ruff format
