lint:
    ruff check 
    mypy
    codespell src examples
    bandit -c pyproject.toml -r src
    slotscheck src

format:
    ruff format
